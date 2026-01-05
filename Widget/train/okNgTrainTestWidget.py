from __future__ import annotations
from typing import Dict, List, Optional, Tuple, Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QCheckBox, QSizePolicy


ClassSpec = Union[str, Tuple[str, int], Dict[str, object]]
# 允许传入:
#   "OK1(1000)" 或 ("OK1",1000) 或 {"name":"OK1","count":1000}


class OkNgTrainTestWidget(QWidget):
    """
    Grid 布局严格对齐你给的 UI:
      row0: (col3) Train, (col4) Test
      row1: OK 行: col0=OK:  col1-2=OK子类文本  col3=train cb col4=test cb
      row2: NG 行: col0=NG:  col1-2=NG子类文本  col3=train cb(禁用) col4=test cb
    如果 OK/NG 下有多个小类，则 OK/NG 会各占多行（每个小类一行），但列位置完全一致。
    """

    stateChanged = Signal(dict)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        sp = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setSizePolicy(sp)

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(10, 10, 10, 10)
        self.grid.setHorizontalSpacing(18)
        self.grid.setVerticalSpacing(6)

        # (major, sub_key) -> (label_major, label_text, cb_train, cb_test)
        self._rows: Dict[Tuple[str, str], Tuple[QLabel, QLabel, QCheckBox, QCheckBox]] = {}

        self._build_header()

    # ---------- public ----------
    def set_rows(self, ok: List[ClassSpec], ng: List[ClassSpec]):
        """重建行：OK/NG 固定，但小类数量可变。"""
        self._clear_dynamic()
        self._build_header()

        row = 1
        row = self._add_major_rows("OK", ok, row)
        row = self._add_major_rows("NG", ng, row)

        self.stateChanged.emit(self.to_state())

    def set_state(self, state: dict):
        """
        推荐 state:
        {
          "OK": {"OK1": {"train": True, "test": False}, ...},
          "NG": {"NG1": {"test": True}, ...}
        }
        兼容:
          {"OK": {"OK1": [True, False]}, "NG": {"NG1": [False, True]}}
        """
        for (major, sub), (_lmaj, _ltxt, cb_tr, cb_te) in self._rows.items():
            item = (state.get(major, {}) or {}).get(sub, {})

            train = False
            test = False
            if isinstance(item, dict):
                train = bool(item.get("train", False))
                test = bool(item.get("test", False))
            elif isinstance(item, (list, tuple)) and len(item) >= 2:
                train = bool(item[0])
                test = bool(item[1])

            if major == "NG":
                train = False  # 强制

            cb_tr.blockSignals(True)
            cb_te.blockSignals(True)
            cb_tr.setChecked(train)
            cb_te.setChecked(test)
            cb_tr.blockSignals(False)
            cb_te.blockSignals(False)

        self.stateChanged.emit(self.to_state())

    def to_state(self) -> dict:
        out = {"OK": {}, "NG": {}}
        for (major, sub), (_lmaj, _ltxt, cb_tr, cb_te) in self._rows.items():
            out[major][sub] = {
                "train": bool(cb_tr.isChecked()) if major == "OK" else False,
                "test": bool(cb_te.isChecked()),
            }
        return out

    # ---------- internal ----------
    def _build_header(self):
        # row 0 col 3/4: Train/Test
        lbl_train = QLabel("训练")
        lbl_test = QLabel("测试")
        lbl_train.setAlignment(Qt.AlignCenter)
        lbl_test.setAlignment(Qt.AlignCenter)

        self.grid.addWidget(lbl_train, 0, 3, 1, 1)
        self.grid.addWidget(lbl_test, 0, 4, 1, 1)

    def _add_major_rows(self, major: str, specs: List[ClassSpec], start_row: int) -> int:
        # major 标签只在该 major 的第一行显示，其余行留空（看起来更像你图里）
        first = True
        for spec in specs:
            sub_key, show_text = self._normalize_spec(spec)

            lbl_major = QLabel(f"{major}:") if first else QLabel("")
            lbl_major.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            lbl_text = QLabel(show_text)
            lbl_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            cb_train = QCheckBox()
            cb_test = QCheckBox()

            # NG 的 train 不允许
            if major == "NG":
                cb_train.setEnabled(False)
                cb_train.setChecked(False)

            r = start_row
            # col0: major
            self.grid.addWidget(lbl_major, r, 0, 1, 1)
            # col1-2: text (span 2)  —— 对齐你代码 addWidget(lblGoodCount_4, 1,1,1,2)
            self.grid.addWidget(lbl_text, r, 1, 1, 2)
            # col3/4: checkboxes
            self.grid.addWidget(cb_train, r, 3, 1, 1, alignment=Qt.AlignCenter)
            self.grid.addWidget(cb_test, r, 4, 1, 1, alignment=Qt.AlignCenter)

            self._rows[(major, sub_key)] = (lbl_major, lbl_text, cb_train, cb_test)

            cb_train.stateChanged.connect(self._emit_state)
            cb_test.stateChanged.connect(self._emit_state)

            start_row += 1
            first = False

        # 如果某个 major 没有任何小类，也给它显示一行（可选）
        if not specs:
            lbl_major = QLabel(f"{major}:")
            lbl_text = QLabel("--")
            cb_train = QCheckBox()
            cb_test = QCheckBox()
            if major == "NG":
                cb_train.setEnabled(False)
                cb_train.setChecked(False)

            self.grid.addWidget(lbl_major, start_row, 0, 1, 1)
            self.grid.addWidget(lbl_text, start_row, 1, 1, 2)
            self.grid.addWidget(cb_train, start_row, 3, 1, 1, alignment=Qt.AlignCenter)
            self.grid.addWidget(cb_test, start_row, 4, 1, 1, alignment=Qt.AlignCenter)

            # 不写入 _rows（因为没 sub_key）
            start_row += 1

        return start_row

    def _emit_state(self, *_):
        # 确保 NG train 永远为 False
        for (major, _), (_lmaj, _ltxt, cb_tr, _cb_te) in self._rows.items():
            if major == "NG" and cb_tr.isChecked():
                cb_tr.blockSignals(True)
                cb_tr.setChecked(False)
                cb_tr.blockSignals(False)
        self.stateChanged.emit(self.to_state())

    def _clear_dynamic(self):
        # 清掉所有布局控件（包括表头），重建更稳
        while self.grid.count():
            it = self.grid.takeAt(0)
            w = it.widget()
            if w:
                w.deleteLater()
            del it
        self._rows.clear()

    @staticmethod
    def _normalize_spec(spec: ClassSpec) -> Tuple[str, str]:
        if isinstance(spec, str):
            key = spec.split("(")[0].strip()
            return key, spec
        if isinstance(spec, tuple) and len(spec) >= 2:
            name, count = str(spec[0]), int(spec[1])
            return name, f"{name}({count})"
        if isinstance(spec, dict):
            name = str(spec.get("name", ""))
            count = spec.get("count", None)
            return (name, f"{name}({int(count)})") if count is not None else (name, name)
        s = str(spec)
        return s, s

# w = OkNgSplitSelectWidget()
# w.set_rows(
#     ok=[("OK1", 1000), ("OK2", 200)],
#     ng=[("NG", 200)]
# )
#
# # UI -> dict
# print(w.to_state())
#
# # dict -> UI
# w.set_state({
#     "OK": {"OK1": {"train": True, "test": False}, "OK2": {"train": False, "test": True}},
#     "NG": {"NG": {"test": True}}
# })