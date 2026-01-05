# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindowUI.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTabWidget,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1067, 777)
        self.newPjtAct = QAction(MainWindow)
        self.newPjtAct.setObjectName(u"newPjtAct")
        self.openPjtAct = QAction(MainWindow)
        self.openPjtAct.setObjectName(u"openPjtAct")
        self.sysSettingAct = QAction(MainWindow)
        self.sysSettingAct.setObjectName(u"sysSettingAct")
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.imgTab = QWidget()
        self.imgTab.setObjectName(u"imgTab")
        self.tabWidget.addTab(self.imgTab, "")
        self.trainTab = QWidget()
        self.trainTab.setObjectName(u"trainTab")
        self.tabWidget.addTab(self.trainTab, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1067, 33))
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menu.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.newPjtAct)
        self.menu.addAction(self.openPjtAct)
        self.menu.addSeparator()
        self.menu.addAction(self.sysSettingAct)
        self.menu.addSeparator()
        self.menu.addAction(self.action)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AI\u5916\u89c2\u68c0\u67e5BOX", None))
        self.newPjtAct.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u9879\u76ee", None))
        self.openPjtAct.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u9879\u76ee", None))
        self.sysSettingAct.setText(QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u8bbe\u7f6e", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.imgTab), QCoreApplication.translate("MainWindow", u"\u56fe\u5e93", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.trainTab), QCoreApplication.translate("MainWindow", u"\u8bad\u7ec3", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u".", None))
    # retranslateUi

