# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'imgGalleryUI.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QPushButton, QScrollArea, QSizePolicy, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1308, 638)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.importImgBtn = QPushButton(self.frame_2)
        self.importImgBtn.setObjectName(u"importImgBtn")
        self.importImgBtn.setMinimumSize(QSize(200, 40))

        self.verticalLayout.addWidget(self.importImgBtn)

        self.delImgBtn = QPushButton(self.frame_2)
        self.delImgBtn.setObjectName(u"delImgBtn")
        self.delImgBtn.setMinimumSize(QSize(200, 40))

        self.verticalLayout.addWidget(self.delImgBtn)

        self.pjtInfoFrame = QFrame(self.frame_2)
        self.pjtInfoFrame.setObjectName(u"pjtInfoFrame")
        self.pjtInfoFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.pjtInfoFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.pjtInfoFrame)

        self.treeWidget = QTreeWidget(self.frame_2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setHeaderHidden(True)

        self.verticalLayout.addWidget(self.treeWidget)


        self.horizontalLayout.addWidget(self.frame_2)

        self.imgScrollArea = QScrollArea(Form)
        self.imgScrollArea.setObjectName(u"imgScrollArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.imgScrollArea.sizePolicy().hasHeightForWidth())
        self.imgScrollArea.setSizePolicy(sizePolicy1)
        self.imgScrollArea.setMinimumSize(QSize(1000, 0))
        self.imgScrollArea.setMaximumSize(QSize(16777215, 16777212))
        self.imgScrollArea.setStyleSheet(u"background-color: rgb(64, 64, 64);")
        self.imgScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.imgScrollArea.setWidgetResizable(True)
        self.imgScrollArea.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1004, 618))
        self.scrollAreaWidgetContents_2.setMinimumSize(QSize(1000, 0))
        self.imgScrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.horizontalLayout.addWidget(self.imgScrollArea)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.importImgBtn.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165\u56fe\u50cf", None))
        self.delImgBtn.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u56fe\u50cf", None))
    # retranslateUi

