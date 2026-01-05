from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPixmap, QFontMetrics
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QToolButton


class ImageItemWidget(QWidget):
    """
        上图下名 + 可选按钮 + 双击事件
        - set_path(path): imageLabel 显示图片，textLabel 显示文件名
        - 单击任意处：选中（checkbox-like）
        - 双击：发出 doubleClicked(path)
        """
    clicked = Signal(str, bool)  # path, checked (单击toggle后发)
    doubleClicked = Signal(str)  # path (双击仅打开详情，不改勾选)
    checkedChanged = Signal(bool)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._path = ""
        self._checked = False

        # --- UI ---
        self.imageLabel = QLabel(alignment=Qt.AlignCenter)
        self.imageLabel.setFixedSize(160, 120)
        self.imageLabel.setStyleSheet("background:#3a3a3a;")
        self.imageLabel.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.textLabel = QLabel(alignment=Qt.AlignCenter)
        self.textLabel.setFixedHeight(18)
        self.textLabel.setStyleSheet("color:white;")
        self.textLabel.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        lay.addWidget(self.imageLabel)
        lay.addWidget(self.textLabel)

        # --- checkbox-like button ---
        self.selectBtn = QToolButton(self)
        self.selectBtn.setCheckable(True)
        self.selectBtn.setAutoRaise(True)
        self.selectBtn.setFixedSize(18, 18)
        self.selectBtn.setCursor(Qt.PointingHandCursor)
        self.selectBtn.setText("✓")
        self.selectBtn.setStyleSheet("""
                QToolButton {
                    border: 1px solid rgba(255,255,255,0.6);
                    border-radius: 9px;
                    background: rgba(0,0,0,0.35);
                    color: transparent;
                    font-weight: 700;
                }
                QToolButton:checked {
                    background: rgba(0,163,255,0.85);
                    border: 1px solid rgba(0,163,255,1);
                    color: white;
                }
            """)
        # 点按钮：立刻toggle（不走单击/双击定时逻辑）
        self.selectBtn.clicked.connect(lambda: self.setChecked(self.selectBtn.isChecked()))

        self.setCursor(Qt.PointingHandCursor)
        self._apply_checked_style()

        # --- 单击/双击区分：单击延迟提交，双击会取消 ---
        self._click_timer = QTimer(self)
        self._click_timer.setSingleShot(True)
        self._click_timer.timeout.connect(self._commit_single_click)
        self._pending_click = False

    # ---- API ----
    def set_path(self, path: str):
        self._path = path or ""
        self.textLabel.setText(os.path.basename(self._path) if self._path else "")

        pm = QPixmap(self._path) if self._path else QPixmap()
        if pm.isNull():
            self.imageLabel.clear()
        else:
            self.imageLabel.setPixmap(pm.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def path(self) -> str:
        return self._path

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, checked: bool):
        checked = bool(checked)
        if self._checked == checked:
            return
        self._checked = checked
        self.selectBtn.setChecked(checked)
        self._apply_checked_style()
        self.checkedChanged.emit(self._checked)

    def toggleChecked(self):
        self.setChecked(not self._checked)

    # ---- layout ----
    def resizeEvent(self, e):
        super().resizeEvent(e)
        r = self.imageLabel.geometry()
        self.selectBtn.move(r.left() + 6, r.top() + 6)

    # ---- events ----
    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        # 不在 press 里做 toggle，避免双击触发两次
        if e.button() == Qt.LeftButton and not self.selectBtn.geometry().contains(e.pos()):
            self._pending_click = True

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if e.button() != Qt.LeftButton:
            return
        if self.selectBtn.geometry().contains(e.pos()):
            return  # 点按钮交给按钮处理
        if self._pending_click:
            # 延迟一点：如果用户实际上是双击，doubleClick 会先来并 stop timer
            self._click_timer.start(180)

    def mouseDoubleClickEvent(self, e):
        super().mouseDoubleClickEvent(e)
        if e.button() == Qt.LeftButton:
            # ✅ 双击：只打开详情，不改勾选
            self._pending_click = False
            self._click_timer.stop()
            self.doubleClicked.emit(self._path)

    def _commit_single_click(self):
        if not self._pending_click:
            return
        self._pending_click = False
        self.toggleChecked()
        self.clicked.emit(self._path, self._checked)

    def _apply_checked_style(self):
        self.setStyleSheet(
            "ImageThumbItem{border:2px solid #00A3FF;border-radius:6px;background:rgba(255,255,255,0.03);}"
            if self._checked else
            "ImageThumbItem{border:2px solid transparent;border-radius:6px;background:transparent;}"
        )