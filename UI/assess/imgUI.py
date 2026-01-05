# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'imgUI.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(775, 262)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.imgCvtButton = QPushButton(Form)
        self.imgCvtButton.setObjectName(u"imgCvtButton")

        self.horizontalLayout_6.addWidget(self.imgCvtButton)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(0, 180))
        self.scrollArea.setStyleSheet(u"background-color: rgb(64, 64, 64);")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 757, 180))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollArea)

        self.pageLayout = QHBoxLayout()
        self.pageLayout.setObjectName(u"pageLayout")
        self.firstPageBtn = QPushButton(Form)
        self.firstPageBtn.setObjectName(u"firstPageBtn")

        self.pageLayout.addWidget(self.firstPageBtn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.pageLayout.addItem(self.horizontalSpacer)

        self.prevBtn = QPushButton(Form)
        self.prevBtn.setObjectName(u"prevBtn")

        self.pageLayout.addWidget(self.prevBtn)

        self.pageLab = QLabel(Form)
        self.pageLab.setObjectName(u"pageLab")

        self.pageLayout.addWidget(self.pageLab)

        self.nextBtn = QPushButton(Form)
        self.nextBtn.setObjectName(u"nextBtn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.nextBtn.sizePolicy().hasHeightForWidth())
        self.nextBtn.setSizePolicy(sizePolicy1)

        self.pageLayout.addWidget(self.nextBtn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.pageLayout.addItem(self.horizontalSpacer_2)

        self.lastPageBtn = QPushButton(Form)
        self.lastPageBtn.setObjectName(u"lastPageBtn")
        sizePolicy1.setHeightForWidth(self.lastPageBtn.sizePolicy().hasHeightForWidth())
        self.lastPageBtn.setSizePolicy(sizePolicy1)

        self.pageLayout.addWidget(self.lastPageBtn)


        self.verticalLayout.addLayout(self.pageLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.imgCvtButton.setText(QCoreApplication.translate("Form", u"\u70ed\u56fe", None))
        self.firstPageBtn.setText(QCoreApplication.translate("Form", u"|\u25c0", None))
        self.prevBtn.setText(QCoreApplication.translate("Form", u"\u25c0", None))
        self.pageLab.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.nextBtn.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.lastPageBtn.setText(QCoreApplication.translate("Form", u"\u25b6|", None))
    # retranslateUi

