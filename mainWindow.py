from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
    QMainWindow,
    QMessageBox,
)

from Application.ProjectDataClass import Project
from Infrastructure.sqlDB import SqlDB
from Interface.UI.mainWindowUI import Ui_MainWindow
from Interface.Widget.createPjtDialog import CreatePjtDialog
from Interface.Widget.imgGallery.imgGallery import ImgGallery
from Interface.Widget.train.trainWidget import TrainWidget
from Interface.qtBridge import QtBridge


class MainWindow(QMainWindow):
    def __init__(
            self,
            sql_db: Optional[SqlDB] = None,
            bridge: Optional[QtBridge] = None,
            parent=None,
    ):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.sql_db = sql_db
        self.bridge = bridge
        self.project = None
        self._ui_init()
        self._setup_tabs()

        # 新建项目
        self.ui.newPjtAct.triggered.connect(self._new_pjt_dialog)
        # 打开项目
        self.ui.openPjtAct.triggered.connect(self._open_pjt_dialog)

        # 切换tab页
        self.ui.tabWidget.currentChanged.connect(self._on_tab_changed)

    @Slot()
    def _new_pjt_dialog(self):
        dialog = CreatePjtDialog(self, self.sql_db)
        result = dialog.exec()
        if result:
            self.project = dialog.project
            self.img_gallery.set_project(self.project)
            self.train_gallery.set_project(self.project)

    @Slot()
    def _open_pjt_dialog(self):
        if self.sql_db is None:
            QMessageBox.warning(self, "打开项目", "数据库未初始化，无法获取项目列表")
            return

        projects = self.sql_db.fetch_all("project", columns='*')
        if not projects:
            QMessageBox.information(self, "打开项目", "当前没有可用项目，请先创建项目")
            return
        project_map = {str(row["name"]): Project(*row) for row in projects}
        names = list(project_map.keys())
        name, ok = QInputDialog.getItem(self, "打开项目", "选择项目", names, 0, False)
        if ok and name:
            self.project = project_map[name]
            self.img_gallery.set_project(self.project)

    @Slot(int)
    def _on_tab_changed(self, index: int):
        widget = self.ui.tabWidget.widget(index)
        if widget is self.train_gallery:
            self.train_gallery.set_project(self.project)

    def _ui_init(self):
        self.ui.menu.setIcon(QIcon(r"D:\CODE\Train\src\img\menu.svg"))

    def _setup_tabs(self):
        # 重新挂载图库、训练页到主页面
        self.img_gallery = ImgGallery(sql_db=self.sql_db, bridge=self.bridge, project=self.project, parent=self)
        img_tab_index = self.ui.tabWidget.indexOf(self.ui.imgTab)
        if img_tab_index != -1:
            self.ui.tabWidget.removeTab(img_tab_index)

        self.ui.tabWidget.insertTab(0, self.img_gallery, "数据管理")

        self.train_gallery = TrainWidget(sql_db=self.sql_db,bridge=self.bridge, project=self.project, parent=self)
        train_tab_index = self.ui.tabWidget.indexOf(self.ui.trainTab)
        if train_tab_index != -1:
            self.ui.tabWidget.removeTab(train_tab_index)

        self.ui.tabWidget.insertTab(1, self.train_gallery, "模型训练")


if __name__ == '__main__':
    app = QApplication([])

    w = MainWindow()
    w.setWindowTitle("main")
    w.resize(1200, 800)
    w.show()

    app.exec()
