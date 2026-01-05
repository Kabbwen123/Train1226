from __future__ import annotations
from pathlib import Path
from typing import List, Optional

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QTreeWidgetItem, QPushButton,
    QLayoutItem, QMessageBox,
)

from Application.ProjectDataClass import Project, Image, ImgDetailData
from Infrastructure.sqlDB import SqlDB
from Interface.UI.imgGallery.imgGalleryUI import Ui_Form
from Interface.Widget.imgDetailWidget import ImgDetailDialog
from Interface.Widget.imgGallery.imgItemWidget import ImageItemWidget
from Interface.Widget.imgGallery.imgImportDialog import ImgImportDialog
from Interface.Widget.pjtInfoWidget import PjtInfoWidget
from Interface.qtBridge import QtBridge


class FlowGridContainer(QWidget):
    """按容器宽度自动换行的网格容器（保持顺序左->右，上->下）"""

    def __init__(
            self,
            item_w: int,
            item_h: int,
            h_spacing: int = 20,
            v_spacing: int = 20,
            margins=(8, 8, 8, 8),
            parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self._items: List[QWidget] = []
        self._item_w = item_w
        self._item_h = item_h

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(*margins)
        self.grid.setHorizontalSpacing(h_spacing)
        self.grid.setVerticalSpacing(v_spacing)
        self.grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self._last_cols = -1

    def set_items(self, widgets: List[QWidget]):
        # 1) 删除旧 widgets（否则仍会显示）
        for w in self._items:
            w.setParent(None)
            w.deleteLater()
        self._items.clear()

        # 2) 清空布局里的 layout item
        self._clear_layout_only()

        # 3) 设置新 widgets
        self._items = widgets[:]
        for w in self._items:
            w.setParent(self)
            w.show()

        # 4) 强制重排 + 更新几何
        self._last_cols = -1
        self._relayout(force=True)
        self.grid.invalidate()
        self.updateGeometry()
        self.update()

    def add_item(self, w: QWidget):
        w.setParent(self)
        self._items.append(w)
        self._relayout(force=True)

    def items(self) -> List[QWidget]:
        return self._items

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._relayout()

    def _calc_cols(self) -> int:
        ml, mt, mr, mb = self.grid.getContentsMargins()
        avail = max(1, self.width() - ml - mr)
        hs = self.grid.horizontalSpacing()
        # cols * item_w + (cols-1)*hs <= avail  =>  cols <= (avail + hs) / (item_w + hs)
        cols = max(1, (avail + hs) // (self._item_w + hs))
        return int(cols)

    def _relayout(self, force: bool = False):
        cols = self._calc_cols()
        if not force and cols == self._last_cols:
            return
        self._last_cols = cols

        self._clear_layout_only()
        for idx, w in enumerate(self._items):
            r = idx // cols
            c = idx % cols
            self.grid.addWidget(w, r, c)

    def _clear_layout_only(self):
        # 只从 layout 里拿掉 item，不删除 widget
        while self.grid.count():
            it: QLayoutItem = self.grid.takeAt(0)
            # 不要 deleteLater，这样重排能复用同一批 widget
            # w = it.widget()
            # if w: w.setParent(self)
            del it


class ImgGallery(QWidget, Ui_Form):
    imageClicked = Signal(dict)
    imageDoubleClicked = Signal(dict)

    TAGS = ("OK", "NG")
    ITEM_W = 160
    ITEM_H = 120 + 10 + 10 + 18

    def __init__(self,
                 sql_db: Optional[SqlDB] = None,
                 bridge: Optional[QtBridge] = None,
                 project: Optional[Project] = None,
                 parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.sql_db = sql_db
        self.project = project
        self.bridge = bridge

        self._init_img_area()
        self._init_tree()

        # 当前展示的所有图
        self.cur_imgs = []

        self.treeWidget.itemClicked.connect(self._on_tree_item_clicked)
        self.importImgBtn.clicked.connect(self._import_img)
        self.delImgBtn.clicked.connect(self._delete_selected_images)
        self.delImgBtn.setEnabled(False)

        self._reload_project_images()

    @Slot()
    def _import_img(self):
        dlg = ImgImportDialog(self, sql_db=self.sql_db, bridge=self.bridge, project=self.project)
        dlg.import_finished.connect(self._reload_project_images)
        dlg.exec()

    def set_project(self, project: Optional[Project]):
        self.project = project
        v_layout = QVBoxLayout(self.pjtInfoFrame)
        v_layout.addWidget(PjtInfoWidget(project))
        self._reload_project_images()

    # ---------- init ----------
    def _init_img_area(self):

        self.image_container = FlowGridContainer(item_w=self.ITEM_W, item_h=self.ITEM_H)

        self.imgScrollArea.setWidgetResizable(True)
        self.imgScrollArea.setWidget(self.image_container)

    def _init_tree(self):
        self.treeWidget.clear()
        self.treeWidget.setStyleSheet(
            """
            QTreeWidget::item:selected {
                background-color: #2f6fed;
                color: white;
            }
            QTreeWidget::item:selected:active {
                background-color: #2f6fed;
                color: white;
            }
            QTreeWidget::item:selected:!active {
                background-color: #2f6fed;
                color: white;
            }
            QPushButton {
                text-align: left;
                padding: 2px 6px;
                border-radius: 4px;
            }
            QPushButton[treeItemSelected="true"] {
                background-color: #2f6fed;
                color: white;
            }
            """
        )
        self._selected_subtag_btn: Optional[QPushButton] = None
        self.tree_roots: dict[str, QTreeWidgetItem] = {}
        for tag in self.TAGS:
            root = QTreeWidgetItem([tag])
            root.setExpanded(True)
            self.treeWidget.addTopLevelItem(root)
            self.tree_roots[tag] = root

    # ---------- data ----------
    def _reload_project_images(self):
        self._clear_tree_subtags()

        if not self.project or not self.sql_db:
            return

        self._populate_tree_subtags()
        self._display_images()  # 默认显示全部

    def _populate_tree_subtags(self):
        records = self.sql_db.fetch_all(
            "image",
            columns='DISTINCT "tag","subtag"',
            where_clause='"project_id" = ?',
            params=[self.project.id],
        )
        for r in records:
            tag = (r["tag"] or "")
            subtag = (r["subtag"] or "")
            if tag in self.tree_roots:
                self._add_subtag(tag, subtag)

    def _add_subtag(self, tag: str, subtag: str):
        root = self.tree_roots[tag]
        child = QTreeWidgetItem(root)
        child.setText(0, "")  # 用按钮显示

        btn = QPushButton(subtag or "未命名")
        btn.setFlat(True)
        btn.clicked.connect(
            lambda _=False, t=tag, s=subtag, i=child, b=btn: self._on_subtag_clicked(i, b, t, s)
        )
        self.treeWidget.setItemWidget(child, 0, btn)

    def _get_images(self, tag: str | None = None, subtag: str | None = None):
        if not self.project or not self.sql_db:
            return []

        where = ['"project_id" = ?']
        params: list = [self.project.id]
        if tag:
            where.append('"tag" = ?')
            params.append(tag)
        if subtag:
            where.append('"subtag" = ?')
            params.append(subtag)

        return self.sql_db.fetch_all("image", where_clause=" AND ".join(where), params=params)

    # ---------- ui behavior ----------
    def _on_tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        if item.parent() is None:
            tag = item.text(0)
            if tag:
                self._set_selected_subtag_button(None)
                self._display_images(tag, None)

    def _display_images(self, tag: str | None = None, subtag: str | None = None):
        images = self._get_images(tag, subtag)
        widgets = []
        self.cur_imgs = []
        for i, img in enumerate(images):
            img = Image(*img)
            path = img.path_convert
            info = f"图片名：{img.name}\n标签：{img.tag}\n子标签：{img.subtag}"
            img_data = ImgDetailData(path, None, info, img)

            self.cur_imgs.append(img_data)

            item = ImageItemWidget()
            item.setFixedSize(self.ITEM_W, self.ITEM_H)  # 关键：固定尺寸，换行计算才准确
            item.set_path(path)
            item.doubleClicked.connect(lambda *args, index=i: self.open_img_detail(index))
            item.checkedChanged.connect(self._update_delete_btn_state)
            widgets.append(item)
        self.image_container.set_items(widgets)
        self._update_delete_btn_state()

    def _on_subtag_clicked(self, item: QTreeWidgetItem, btn: QPushButton, tag: str, subtag: str):
        self.treeWidget.setCurrentItem(item)
        self._set_selected_subtag_button(btn)
        self._display_images(tag, subtag)

    def _set_selected_subtag_button(self, btn: Optional[QPushButton]):
        if self._selected_subtag_btn is btn:
            return
        if self._selected_subtag_btn is not None:
            self._selected_subtag_btn.setProperty("treeItemSelected", False)
            self._selected_subtag_btn.style().unpolish(self._selected_subtag_btn)
            self._selected_subtag_btn.style().polish(self._selected_subtag_btn)
            self._selected_subtag_btn.update()
        self._selected_subtag_btn = btn
        if btn is not None:
            btn.setProperty("treeItemSelected", True)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    @Slot()
    def _delete_selected_images(self):
        if not self.cur_imgs:
            return

        checked_indices = [idx for idx, widget in enumerate(self.image_container.items()) if
                           getattr(widget, "isChecked", lambda: False)()]
        if not checked_indices:
            return

        confirm = QMessageBox.question(
            self,
            "删除图片",
            "确认删除选中的图片？此操作不可恢复。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        for idx in sorted(checked_indices, reverse=True):
            if idx >= len(self.cur_imgs):
                continue

            img = self.cur_imgs[idx]
            image_id = img.datas.id
            image_path = img.path

            if image_path:
                try:
                    path_obj = Path(image_path)
                    if path_obj.exists():
                        path_obj.unlink()
                except Exception:
                    pass

            if self.sql_db is not None and image_id is not None:
                try:
                    self.sql_db.delete("image", '"id" = ?', [image_id])
                except Exception:
                    pass

        self._reload_project_images()
        self._update_delete_btn_state()

    def _update_delete_btn_state(self):
        has_checked = any(getattr(widget, "isChecked", lambda: False)() for widget in self.image_container.items())
        self.delImgBtn.setEnabled(has_checked)

    def open_img_detail(self, index):
        dlg = ImgDetailDialog(self.cur_imgs, index=index, sql_db=self.sql_db)
        dlg.exec()
        self._reload_project_images()

    # ---------- helpers ----------
    def _clear_tree_subtags(self):
        if not hasattr(self, "tree_roots"):
            return
        self._set_selected_subtag_button(None)
        for root in self.tree_roots.values():
            for i in range(root.childCount() - 1, -1, -1):
                child = root.child(i)
                w = self.treeWidget.itemWidget(child, 0)
                if w:
                    w.deleteLater()
                    self.treeWidget.setItemWidget(child, 0, None)
                root.removeChild(child)

    @staticmethod
    def _clear_layout(layout: QGridLayout):
        while layout.count():
            it = layout.takeAt(0)
            w = it.widget()
            if w:
                w.deleteLater()

    @staticmethod
    def _row_to_dict(row):
        # sqlite3.Row -> dict
        return dict(zip(row.keys(), row))
