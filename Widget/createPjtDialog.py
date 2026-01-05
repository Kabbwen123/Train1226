import os
import sqlite3
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QMessageBox, QFileDialog, QGraphicsScene

from Application.ProjectDataClass import Project
from Config.constant import TYPE
from Infrastructure.fileHandle import copy_file_to_folder
from Interface.UI.createPjtUI import Ui_Dialog


class CreatePjtDialog(QDialog, Ui_Dialog):
    def __init__(
            self,
            parent=None,
            sql_db=None,
    ):
        super().__init__(parent)
        self.setupUi(self)  # 初始化UI

        self.sql_db = sql_db
        self.project: Project | None = None

        self.template_path = None
        self.mask_path = None

        self.templateFileBtn.clicked.connect(self._file_template)
        self.maskFileBtn.clicked.connect(self._file_mask)
        self.confirmBtn.clicked.connect(self._new_project)
        self.cancelBtn.clicked.connect(self.reject)

        self.pjtTypeCbx.addItem(TYPE.EXCEPTION_CHECK.label, TYPE.EXCEPTION_CHECK.code)

        # 缩略图显示
        # 1) 给两个 QGraphicsView 配 scene
        self._tmpl_scene = QGraphicsScene(self.templatePreview)
        self.templatePreview.setScene(self._tmpl_scene)

        self._mask_scene = QGraphicsScene(self.maskPreview)
        self.maskPreview.setScene(self._mask_scene)

        # 初始显示提示
        self._set_view_image(self.templatePreview, self._tmpl_scene, None)
        self._set_view_image(self.maskPreview, self._mask_scene, None)

        # 2) 可选：更像“预览框”的显示效果
        self.templatePreview.setRenderHints(self.templatePreview.renderHints())
        self.maskPreview.setRenderHints(self.maskPreview.renderHints())
        self.templatePreview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.maskPreview.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def file_copy_img(self, project_name):
        project_dir = Path("Project") / project_name
        template_dir = project_dir / "Template"
        template_dir.mkdir(parents=True, exist_ok=True)
        if self.template_path and self.mask_path:
            self.template_path = copy_file_to_folder(self.template_path, template_dir)
            self.mask_path = copy_file_to_folder(self.mask_path, template_dir)
        else:
            QMessageBox.warning(self, "新建项目", "未导入完整模板文件")
            return

    @Slot()
    def _file_template(self):
        path = self._open_to_choose_file()
        if path is not None:
            self.template_path = path
            self._set_view_image(self.templatePreview, self._tmpl_scene, self.template_path)

    @Slot()
    def _file_mask(self):
        path = self._open_to_choose_file()
        if path is not None:
            self.mask_path = path
            self._set_view_image(self.maskPreview, self._mask_scene, self.mask_path)

    def _new_project(self):
        name = self.pjtNameEdit.text().strip()
        p_type = self.pjtTypeCbx.currentData()
        if not name:
            QMessageBox.warning(self, "新建项目", "项目名称不能为空")
            return

        # 避免名称重复
        exists = self.sql_db.fetch_one("project", where_clause='"name" = ?', params=[name])
        if exists is not None:
            QMessageBox.critical(self, "新建项目", "项目名称已存在，请更换名称")
            return

        try:
            p_id = self.sql_db.insert("project", {"name": name,
                                                  "type": p_type,
                                                  "template_path": self.template_path,
                                                  "mask_path": self.mask_path,
                                                  "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                  })

            # 模板文件处理
            self.file_copy_img(name)  # 保存模板文件

            self._set_view_image(self.templatePreview, self._tmpl_scene, self.template_path)
            self._set_view_image(self.maskPreview, self._mask_scene, self.mask_path)

            self.project = Project(p_id, name, p_type, self.template_path, self.mask_path,
                                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "新建项目", "项目名称已存在，请更换名称")
        except Exception as e:
            QMessageBox.critical(
                self,
                "新建项目",
                f"新建项目失败: {e}",
            )

    def _open_to_choose_file(self):
        # 弹出文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",  # 起始目录，可以写成 r"D:\TEST" 之类
            "图像文件 (*.png *.jpg *.jpeg *.bmp *.gif);;所有文件 (*.*)"
        )
        if not file_path:  # 用户点了取消
            return None
        return file_path

    def _set_view_image(self, view, scene: QGraphicsScene, path: str | None):
        scene.clear()

        def show_tip(text: str):
            # 在 scene 中间显示提示
            item = scene.addText(text)
            item.setDefaultTextColor(Qt.white)
            font = item.font()
            font.setPointSize(10)
            item.setFont(font)

            scene.setSceneRect(item.boundingRect())
            view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)

        if not path or not os.path.exists(path):
            show_tip("图片导入失败")
            return

        pm = QPixmap(path)
        if pm.isNull():
            show_tip("图片导入失败")
            return

        item = scene.addPixmap(pm)
        scene.setSceneRect(item.boundingRect())  # scene 尺寸=图片尺寸
        view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)  # 自适应缩放

    # 如果窗口大小变化，保持自适应
    def resizeEvent(self, e):
        super().resizeEvent(e)
        if self._tmpl_scene.items():
            self.templatePreview.fitInView(self._tmpl_scene.sceneRect(), Qt.KeepAspectRatio)
        if self._mask_scene.items():
            self.maskPreview.fitInView(self._mask_scene.sceneRect(), Qt.KeepAspectRatio)
