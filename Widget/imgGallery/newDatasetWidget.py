from __future__ import annotations
from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QComboBox,
    QSizePolicy, QFileDialog
)

from Config.constant import DATASET


class NewDatasetWidget(QWidget):
    """
    组合控件：
        [ QComboBox(OK/NG) ] [ QLineEdit(显示目录) ] [ 目录选择 按钮 ] [删除 按钮]
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # ---- QComboBox，等价于 typeCbx ----
        self.typeCbx = QComboBox(self)
        self.typeCbx.setMinimumSize(70, 30)
        self.typeCbx.setMaximumSize(70, 30)
        self.typeCbx.insertItem(DATASET.OK, "OK")
        self.typeCbx.insertItem(DATASET.NG, "NG")
        layout.addWidget(self.typeCbx)

        self.labelEdit = QLineEdit(self)
        sp = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.labelEdit.setSizePolicy(sp)
        self.labelEdit.setMinimumSize(80, 30)
        self.labelEdit.setMaximumSize(80, 30)
        layout.addWidget(self.labelEdit)

        # ---- QLineEdit，等价于 folderEdit ----
        self.folderEdit = QLineEdit(self)
        self.folderEdit.setReadOnly(True)
        self.folderEdit.setSizePolicy(sp)
        self.folderEdit.setMinimumSize(280, 30)
        layout.addWidget(self.folderEdit)

        # ---- QPushButton，等价于 folderBtn ----
        self.folderBtn = QPushButton("目录选择", self)
        self.folderBtn.setSizePolicy(sp)
        self.folderBtn.setMinimumSize(100, 35)
        layout.addWidget(self.folderBtn)

        # ---- QPushButton 删除按钮
        self.deleteBtn = QPushButton("", self)
        self.deleteBtn.setFlat(True)
        self.deleteBtn.setIcon(QIcon(r"/src/img/delete.svg"))
        self.deleteBtn.setIconSize(QSize(20, 24))
        layout.addWidget(self.deleteBtn)

        self.deleteBtn.clicked.connect(self._delete_row)
        self.folderBtn.clicked.connect(self._on_choose_folder)

    # ========== 槽 & 内部方法 ==========

    def _on_choose_folder(self):
        """点击按钮弹出目录选择对话框"""
        folder = QFileDialog.getExistingDirectory(
            self,  # 父窗口
            "选择文件夹",  # 标题
            ""  # 起始目录，不写就是默认
        )
        if not folder:  # 用户点了取消
            return
        self.folderEdit.setText(folder)

    def _delete_row(self):
        """
        从父布局中移除自己，然后销毁：
        这样这行在界面上就消失了。
        """
        parent = self.parentWidget()
        if parent is None:
            # 没有父控件，直接销毁自己
            self.deleteLater()
            return

        layout = parent.layout()
        if layout is not None:
            # 在父布局里找到自己并移除
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item is not None and item.widget() is self:
                    layout.takeAt(i)  # 把这项从布局里拿掉
                    break

        # 解除父子关系并标记删除
        self.setParent(None)
        self.deleteLater()

    # ========== 对外 API：类型 & 路径 ==========

    def return_value(self):
        return (
            self.typeCbx.currentText(),
            self.labelEdit.text(),
            self.folderEdit.text(),
        )
