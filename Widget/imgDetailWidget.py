from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np

from PySide6.QtCore import Qt, QPoint, Slot
from PySide6.QtGui import QPixmap, QImage, QIcon
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QScrollArea, QMessageBox
)

from Application.ProjectDataClass import ImgDetailData
from Interface.UI.imgDetailUI import Ui_Dialog


# ============================================================
# 可缩放 + 可拖动图片控件
# ============================================================
class ZoomableImageView(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._label = QLabel()
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet("background-color: rgb(64, 64, 64);")

        # ScrollArea 里真正显示的 widget
        self.setWidget(self._label)

        self._pixmap_original: QPixmap | None = None
        self._scale_factor: float = 1.0
        self._auto_fit_on_load: bool = True

        self._dragging = False
        self._last_pos: QPoint | None = None

    # ------- 可以直接传 QPixmap 进来（方便做各种处理后再显示） -------
    def set_pixmap(self, pixmap: QPixmap, reset_auto_fit: bool = False):
        if pixmap.isNull():
            return

        self._pixmap_original = pixmap

        if reset_auto_fit or self._auto_fit_on_load:
            self._auto_fit_on_load = True
            self._scale_factor = self._calc_fit_scale()

        self._update_pixmap()

    # ------- 也保留一个从路径加载的接口 -------
    def set_image(self, path: str):
        if not os.path.exists(path):
            self._label.setText(f"找不到文件:\n{path}")
            self._pixmap_original = None
            return

        pm = QPixmap(path)
        if pm.isNull():
            self._label.setText(f"无法加载图片:\n{path}")
            self._pixmap_original = None
            return

        self._pixmap_original = pm

        self._auto_fit_on_load = True
        self._scale_factor = self._calc_fit_scale()

        self._update_pixmap()

    def clear_image(self):
        self._pixmap_original = None
        self._label.clear()

    # ---------- 根据当前 viewport 大小计算自适应缩放比例 ----------

    def _calc_fit_scale(self) -> float:
        if self._pixmap_original is None:
            return 1.0

        vw = self.viewport().width()
        vh = self.viewport().height()
        pw = self._pixmap_original.width()
        ph = self._pixmap_original.height()

        if vw <= 0 or vh <= 0 or pw <= 0 or ph <= 0:
            return 1.0

        scale = min(vw / pw, vh / ph)
        scale = max(0.1, min(scale, 10.0))
        return scale

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._pixmap_original is not None and self._auto_fit_on_load:
            self._scale_factor = self._calc_fit_scale()
            self._update_pixmap()

    # ---------- 缩放 ----------

    def wheelEvent(self, event):
        if self._pixmap_original is None:
            return

        delta = event.angleDelta().y()
        if delta == 0:
            return

        self._auto_fit_on_load = False
        factor = 1.25 if delta > 0 else 0.8
        new_scale = self._scale_factor * factor
        self._scale_factor = max(0.1, min(new_scale, 10.0))
        self._update_pixmap()

    def _update_pixmap(self):
        if self._pixmap_original is None:
            return

        size = self._pixmap_original.size() * self._scale_factor
        scaled = self._pixmap_original.scaled(
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._label.setPixmap(scaled)
        self._label.resize(scaled.size())

    # ---------- 拖动 ----------

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._last_pos = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging and self._last_pos is not None:
            delta = event.position() - self._last_pos
            self._last_pos = event.position()

            hbar = self.horizontalScrollBar()
            vbar = self.verticalScrollBar()

            hbar.setValue(hbar.value() - delta.x())
            vbar.setValue(vbar.value() - delta.y())

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            self._last_pos = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)


# ============================================================
# 适配 imgDetailUI.ui 的图片浏览对话框
# ============================================================
class ImgDetailDialog(QDialog, Ui_Dialog):
    """
    items: List[dict(img info)]
    """

    def __init__(
            self,
            items: List[dict[str, str]] | None = None,
            index: int = 0,
            sql_db=None,
            parent=None,
    ):
        super().__init__(parent)
        self.setupUi(self)

        self._items: List[ImgDetailData] = items or []
        self.sql_db = sql_db

        self._index: int = max(0, min(index, len(self._items) - 1)) if self._items else 0

        # 原始图像（用于亮度/对比度处理）
        self._orig_img: Optional[np.ndarray] = None

        # ---------- 用 ZoomableImageView 替换 ui 里的 imgLab ----------
        self.viewer = ZoomableImageView(self)

        layout = self.horizontalLayout  # imgLab 所在的布局（中间那行）:contentReference[oaicite:2]{index=2}
        layout.replaceWidget(self.imgLab, self.viewer)
        self.imgLab.setParent(None)

        self.deleteBtn.setIcon(QIcon(r"/src/img/delete.svg"))
        # ---------- 上一张 / 下一张按钮 ----------
        for btn in (self.prevBtn, self.nextBtn):
            btn.setFixedSize(44, 44)
            btn.setStyleSheet(
                "QPushButton {"
                "  background-color: rgba(0, 0, 0, 180);"
                "  color: white;"
                "  border: 1px solid rgba(255, 255, 255, 160);"
                "  border-radius: 22px;"
                "  font-size: 20px;"
                "  font-weight: bold;"
                "}"
                "QPushButton:hover {"
                "  background-color: rgba(0, 0, 0, 210);"
                "  border-color: rgba(255, 255, 255, 220);"
                "}"
            )

        self.prevBtn.clicked.connect(self.show_prev)
        self.nextBtn.clicked.connect(self.show_next)
        self.deleteBtn.clicked.connect(self._delete_current_image)

        # ---------- 亮度 / 对比度 Slider 设置 ----------
        # 亮度：-100 ~ 100
        self.horizontalSlider.setRange(-100, 100)
        self.horizontalSlider.setValue(0)

        # 对比度：-100 ~ 100
        self.horizontalSlider_2.setRange(-100, 100)
        self.horizontalSlider_2.setValue(0)

        # 二者变化时都重新渲染当前图片
        self.horizontalSlider.valueChanged.connect(self.on_bc_changed)
        self.horizontalSlider_2.valueChanged.connect(self.on_bc_changed)

        # 初始化显示
        self.refresh()

    # ---------- 导航 ----------

    def show_prev(self):
        if not self._items:
            return
        self._index = (self._index - 1) % len(self._items)
        self.viewer._auto_fit_on_load = True
        self.refresh()

    def show_next(self):
        if not self._items:
            return
        self._index = (self._index + 1) % len(self._items)
        self.viewer._auto_fit_on_load = True
        self.refresh()

    # ---------- 刷新当前图片（切换图片时调用） ----------

    def refresh(self):
        if not self._items:
            self._orig_img = None
            self.viewer.clear_image()
            self.prevBtn.setEnabled(False)
            self.nextBtn.setEnabled(False)
            return

        # TODO 信息完善
        img = self._items[self._index]
        path = img.path
        self.infoLab.setText(img.info)
        # 读原图（BGR）
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            self._orig_img = None
            self.viewer.clear_image()
            return

        self._orig_img = img

        enable_nav = len(self._items) > 1
        self.prevBtn.setEnabled(enable_nav)
        self.nextBtn.setEnabled(enable_nav)

        # 刚切图片时按当前 slider 的亮度/对比度渲染一次
        self.apply_brightness_contrast(reset_fit=True)

    # ---------- Slider 改变时调用 ----------
    def on_bc_changed(self, value: int):
        # 只重新套 LUT，不重新读文件
        self.apply_brightness_contrast(reset_fit=False)

    # ---------- 亮度 / 对比度 实际处理 ----------
    def apply_brightness_contrast(self, reset_fit: bool = False):
        if self._orig_img is None:
            return

        b = self.horizontalSlider.value()  # 亮度：-100 ~ 100
        c = self.horizontalSlider_2.value()  # 对比度：-100 ~ 100

        # 对比度系数：1.0 基准，±100 映射到 [0.0, 2.0]
        alpha = 1.0 + (c / 100.0)
        if alpha < 0:
            alpha = 0.0

        # 亮度偏移
        beta = float(b)

        adjusted = cv2.convertScaleAbs(self._orig_img, alpha=alpha, beta=beta)

        h, w, ch = adjusted.shape
        bytes_per_line = ch * w
        qimg = QImage(adjusted.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)
        pix = QPixmap.fromImage(qimg)

        # 用 viewer 显示处理后的图像。
        # reset_fit=True 时会重新根据窗口自适应（切图时用）
        # reset_fit=False 时保持当前缩放比例（拖 slider 时用）
        self.viewer.set_pixmap(pix, reset_auto_fit=reset_fit)
        # ---------- 删除当前图片 ----------

    @Slot()
    def _delete_current_image(self):
        if not self._items:
            return

        current = self._items[self._index]
        image_id = current.datas.id
        image_path = current.path

        confirm = QMessageBox.question(
            self,
            "删除图片",
            "确认删除当前图片？此操作不可恢复。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

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

        del self._items[self._index]

        if not self._items:
            self.close()
            return

        self._index = min(self._index, len(self._items) - 1)
        self.viewer._auto_fit_on_load = True
        self.refresh()

# ==================== 简单测 试入口 ====================


if __name__ == "__main__":
    app = QApplication(sys.argv)

    demo_items = [
        {"path_convert": r"D:\TEST\yizhao1117\NG (2).jpg", "tag": "1232132", "subtag": "312312"},
        {"path_convert": r"D:\TEST\yizhao1117\NG (3).jpg", "tag": "131231", "subtag": "123123"},
        {"path_convert": r"D:\TEST\yizhao1117\NG (4).jpg", "tag": "123123123", "subtag": "123123"},
    ]

    dlg = ImgDetailDialog(demo_items, index=0)
    dlg.exec()

    sys.exit(0)
