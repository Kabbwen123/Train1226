from __future__ import annotations
from typing import Optional

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy

from Application.ProjectDataClass import Project
from Config.constant import TYPE


class PjtInfoWidget(QWidget):
    """替代 Ui_Form + PjtInfoWidget 的合并简化版"""

    def __init__(self, project: Optional[Project] = None, parent=None):
        super().__init__(parent)

        # ---- UI ----
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        row1 = QHBoxLayout()
        self.pNameLab_2 = QLabel("项目名：")
        self.pNameLab = QLabel("")
        sp = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.pNameLab_2.setSizePolicy(sp)
        self.pNameLab.setSizePolicy(sp)
        row1.addWidget(self.pNameLab_2)
        row1.addWidget(self.pNameLab)
        root.addLayout(row1)

        row2 = QHBoxLayout()
        font20 = QFont()
        font20.setPointSize(20)

        self.pTypeLab_2 = QLabel("项目类型：")
        self.pTypeLab_2.setFont(font20)
        self.pTypeLab = QLabel("")
        self.pTypeLab.setFont(font20)

        self.pTypeLab_2.setSizePolicy(sp)
        self.pTypeLab.setSizePolicy(sp)

        row2.addWidget(self.pTypeLab_2)
        row2.addWidget(self.pTypeLab)
        root.addLayout(row2)

        self.pInfoLab = QLabel("")
        self.pInfoLab.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        root.addWidget(self.pInfoLab)

        # ---- data ----
        self.set_project(project)

    def set_project(self, project: Optional[Project]):
        """外部可随时更新显示内容"""
        if not project:
            self.pNameLab.setText("")
            self.pTypeLab.setText("")
            self.pInfoLab.setText("")
            return

        self.pNameLab.setText(project.name)
        self.pTypeLab.setText(TYPE.from_code(project.type).label)
        self.pInfoLab.setText(f"创建时间：{project.create_time}")
