# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'imgImportUI.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(578, 452)
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.datasetGbx = QGroupBox(Dialog)
        self.datasetGbx.setObjectName(u"datasetGbx")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.datasetGbx.sizePolicy().hasHeightForWidth())
        self.datasetGbx.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.datasetGbx)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.newSetBtn = QPushButton(self.datasetGbx)
        self.newSetBtn.setObjectName(u"newSetBtn")
        self.newSetBtn.setMinimumSize(QSize(0, 35))

        self.horizontalLayout_4.addWidget(self.newSetBtn)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(self.datasetGbx)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(70, 0))
        self.label.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_5.addWidget(self.label)

        self.label_2 = QLabel(self.datasetGbx)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(80, 0))
        self.label_2.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_5.addWidget(self.label_2)

        self.label_3 = QLabel(self.datasetGbx)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(380, 0))
        self.label_3.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_5.addWidget(self.label_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout_3.addWidget(self.datasetGbx)

        self.verticalSpacer = QSpacerItem(20, 56, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.importBtn = QPushButton(Dialog)
        self.importBtn.setObjectName(u"importBtn")
        self.importBtn.setMinimumSize(QSize(0, 35))

        self.horizontalLayout_3.addWidget(self.importBtn)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u5bfc\u5165\u56fe\u50cf", None))
        self.datasetGbx.setTitle(QCoreApplication.translate("Dialog", u"\u6570\u636e\u96c6", None))
        self.newSetBtn.setText(QCoreApplication.translate("Dialog", u"\u65b0\u589e", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u6570\u636e\u96c6\u7c7b\u578b", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u540d\u79f0", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u8def\u5f84", None))
        self.importBtn.setText(QCoreApplication.translate("Dialog", u"\u4e00\u952e\u5bfc\u5165", None))
    # retranslateUi

