import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Sequence, Union, Iterable


class SqlDB:
    def __init__(self,
                 logger,
                 db_path: str,
                 table: Dict,
                 ) -> None:

        self.logger = logger
        self.db_path = db_path
        self.table = table

        # 创建目录和文件
        self._ensure_directory()

        # 建立长期保持的连接（允许多线程）
        self.conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False,
            isolation_level=None  # 自动 commit
        )
        self.conn.row_factory = sqlite3.Row
        # 启用 WAL（写性能更强，同时允许读写并行）
        try:
            self.conn.execute("PRAGMA journal_mode=WAL;")
        except Exception as e:
            self.logger.warning(f"WAL 模式设置失败: {e}")

        # 初始化表
        self._initialize_tables()

    def close(self):
        """程序退出时关闭连接"""
        if self.conn:
            self.conn.close()
            self.logger.info("SQLite 长连接已关闭。")

    # ----------------------------------------------------------------------

    def _ensure_directory(self) -> None:
        path = Path(self.db_path)

        directory = path.parent
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"已创建目录: {directory}")

        if not path.exists():
            path.touch()
            self.logger.info(f"已创建数据库文件: {path}")
        else:
            self.logger.info(f"文件已存在: {path}")

    def _initialize_tables(self) -> None:
        """用长期连接创建表"""
        if not self.table:
            self.logger.warning("未找到表配置，跳过数据库初始化。")
            return
        cursor = self.conn.cursor()
        for table_name, table_config in self.table.items():
            columns_config = table_config.get("column_names", {})
            column_definitions = self._build_column_definitions(columns_config)

            if not column_definitions:
                self.logger.warning(f"表 {table_name} 缺少列定义，已跳过创建。")
                continue

            create_table_sql = (
                f"CREATE TABLE IF NOT EXISTS {table_name} "
                f"({', '.join(column_definitions)});"
            )
            try:
                cursor.execute(create_table_sql)
                self.logger.info(f"表 {table_name} 初始化完成。")
            except sqlite3.Error as exc:
                self.logger.error(f"初始化表 {table_name} 时出错: {exc}")

    def _build_column_definitions(self, columns_config: Dict[str, Union[str, Dict]]) -> List[str]:
        column_definitions: List[str] = []

        for column_name, column_type in columns_config.items():
            if isinstance(column_type, dict):
                # 支持嵌套字典：{"meta": {"a":"TEXT","b":"INTEGER"}} -> meta_a, meta_b
                for nested_name, nested_type in column_type.items():
                    column_definitions.append(f"{column_name}_{nested_name} {nested_type}")
            else:
                column_definitions.append(f"{column_name} {column_type}")
        # 自动补一个自增 id 主键（如果没有手动指定的话）
        if column_definitions and not any(defn.lower().startswith("id ") for defn in column_definitions):
            column_definitions.insert(0, "id INTEGER PRIMARY KEY AUTOINCREMENT")

        return column_definitions

    def _execute(
            self, sql: str, params: Sequence[Any] | None = None
    ) -> sqlite3.Cursor:
        params = params or []
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, params)
            return cursor
        except sqlite3.Error as exc:
            self.logger.error(
                f"SQL 执行失败: {exc}\nSQL: {sql}\nPARAMS: {params}"
            )
            raise

    def _format_columns(self, columns: Iterable[str] | str) -> str:
        if isinstance(columns, str):
            return columns
        return ", ".join(columns)

    # ------------------------------------------------------------------
    # CRUD
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """Insert a row and return the last row id."""
        if not data:
            raise ValueError("字典不能为空")

        cols = ", ".join(f'"{k}"' for k in data.keys())
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"

        cursor = self._execute(sql, tuple(data.values()))
        return cursor.lastrowid

    def insert_many(self, table: str, data: List[Dict[str, Any]]) -> int:
        """Insert multiple rows and return the inserted row count."""
        if not data:
            raise ValueError("数据列表不能为空")

        first_row = data[0]
        if not first_row:
            raise ValueError("数据行不能为空")

        keys = list(first_row.keys())
        if any(row.keys() != first_row.keys() for row in data):
            raise ValueError("所有数据行必须包含相同的字段")

        cols = ", ".join(f'"{k}"' for k in keys)
        placeholders = ", ".join(["?"] * len(keys))
        sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        values = [tuple(row[k] for k in keys) for row in data]

        cursor = self.conn.cursor()
        try:
            cursor.executemany(sql, values)
            return cursor.rowcount
        except sqlite3.Error as exc:
            self.logger.error(
                f"SQL 执行失败: {exc}\nSQL: {sql}\nPARAMS: {values}"
            )
            raise

    def update(
            self,
            table: str,
            data: Dict[str, Any],
            where_clause: str,
            params: Sequence[Any] | None = None,
    ) -> int:
        """Update rows matching the where clause and return affected count."""
        if not data:
            raise ValueError("字典不能为空")
        if not where_clause:
            raise ValueError("更新必须提供 where 条件")

        set_expr = ", ".join(f'"{k}" = ?' for k in data.keys())
        sql = f"UPDATE {table} SET {set_expr} WHERE {where_clause}"

        cursor = self._execute(sql, tuple(data.values()) + tuple(params or []))
        return cursor.rowcount

    def fetch_all(
            self,
            table: str,
            columns: Iterable[str] | str = "*",
            where_clause: str | None = None,
            params: Sequence[Any] | None = None,
    ) -> list[sqlite3.Row]:
        column_sql = self._format_columns(columns)
        sql = f"SELECT {column_sql} FROM {table}"
        if where_clause:
            sql = f"{sql} WHERE {where_clause}"

        cursor = self._execute(sql, params)
        return cursor.fetchall()

    def fetch_one(
            self,
            table: str,
            columns: Iterable[str] | str = "*",
            where_clause: str | None = None,
            params: Sequence[Any] | None = None,
    ) -> sqlite3.Row | None:
        column_sql = self._format_columns(columns)
        sql = f"SELECT {column_sql} FROM {table}"
        if where_clause:
            sql = f"{sql} WHERE {where_clause}"

        cursor = self._execute(sql, params)
        return cursor.fetchone()

    def delete(
            self, table: str, where_clause: str, params: Sequence[Any] | None = None
    ) -> int:
        if not where_clause:
            raise ValueError("删除必须提供 where 条件")

        sql = f"DELETE FROM {table} WHERE {where_clause}"
        cursor = self._execute(sql, params)
        return cursor.rowcount
