import json
import math
import os
from pathlib import Path

import shiboken6
from PySide6.QtCore import Slot, QCoreApplication, Signal
from PySide6.QtWidgets import QDialog, QMessageBox, QProgressDialog

from Application.ProjectDataClass import Project
from Interface.UI.imgGallery.imgImportUI import Ui_Dialog
from Interface.Widget.imgGallery.newDatasetWidget import NewDatasetWidget


class ImgImportDialog(QDialog, Ui_Dialog):
    import_finished = Signal()

    def __init__(
            self,
            parent=None,
            sql_db=None,
            bridge=None,
            project: Project | None = None
    ):
        super().__init__(parent)
        self.setupUi(self)  # 初始化UI

        # 初始化数据集
        self.dataset = []

        self.sql_db = sql_db
        self.project = project
        self.bridge = bridge

        # 导入进度条
        self.progress_dialog: QProgressDialog | None = None

        # 数据集导入
        self.newSetBtn.clicked.connect(self._new_dataset)
        row0 = NewDatasetWidget()
        self.dataset.append(row0)
        self.datasetGbx.layout().addWidget(row0)

        # 一键导入
        self.importBtn.clicked.connect(self._import_img)

        # 接收QT信号
        self.bridge.progress_emitted.connect(self.update_progress)

    @Slot()
    def _new_dataset(self):
        row = NewDatasetWidget()
        self.dataset.append(row)
        self.datasetGbx.layout().addWidget(row)

    @Slot()
    def _import_img(self):
        if self.project is None:
            QMessageBox.warning(self, "导入图像", "未找到可用的项目名称")
            return
        project_dir = Path("Project") / self.project.name
        dataset_dir = project_dir / "Dataset"

        path_list = []
        for row in self.dataset:
            if not shiboken6.isValid(row) or row.parent() is None:  #
                continue
            tag, subtag, path = row.return_value()
            path_list.append((tag, subtag, path))

        self.bridge.transform_img(self.project.template_path, self.project.mask_path, path_list, str(dataset_dir))

    def update_progress(self, folder_index: str, pgs: float, info: dict):
        """
        负责弹出进度条及更新
        """
        if folder_index[0] == "1" and pgs == 0:
            # 生成进度条
            # TODO 参数需修改
            self.progress_dialog = QProgressDialog("正在准备导入...", "Cancel", 0, 1, self)
            self.progress_dialog.setWindowTitle("导入进度")
            self.progress_dialog.setAutoClose(True)
            self.progress_dialog.setCancelButton(None)
            self.progress_dialog.show()
        else:
            # 更新进度条
            if self.progress_dialog is not None:
                self.progress_dialog.setLabelText(f"数据集导入：{folder_index}")
                self.progress_dialog.setValue(math.floor(pgs * 100))
                QCoreApplication.processEvents()
        if info:
            sql_data = []
            for tag, values in info.items():
                for subtag, val_list in values.items():
                    for imgs in val_list:
                        aligned_path = imgs.get("aligned_path","")
                        sql_data.append({
                            "project_id": self.project.id,
                            "name": os.path.basename(aligned_path),
                            "path_convert": aligned_path,
                            "tag": tag,
                            "subtag": subtag,
                        })
            try:
                self.sql_db.insert_many("image", sql_data)
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "导入图像",
                    f"导入图像失败: {e}",
                )

            QMessageBox.information(self, "导入图像", "导入完成")
            self.import_finished.emit()
            self.accept()
