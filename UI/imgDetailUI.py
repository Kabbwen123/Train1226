# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'imgDetailUI.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLayout, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(973, 550)
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.infoLab = QLabel(Dialog)
        self.infoLab.setObjectName(u"infoLab")

        self.horizontalLayout_5.addWidget(self.infoLab)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.deleteBtn = QToolButton(Dialog)
        self.deleteBtn.setObjectName(u"deleteBtn")

        self.horizontalLayout_4.addWidget(self.deleteBtn)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(50, 0))
        self.label.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.label)

        self.horizontalSlider = QSlider(Dialog)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy1)
        self.horizontalSlider.setMinimumSize(QSize(200, 0))
        self.horizontalSlider.setMaximumSize(QSize(200, 16777215))
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.horizontalSlider)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(50, 0))
        self.label_2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.horizontalSlider_2 = QSlider(Dialog)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        sizePolicy1.setHeightForWidth(self.horizontalSlider_2.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_2.setSizePolicy(sizePolicy1)
        self.horizontalSlider_2.setMinimumSize(QSize(200, 0))
        self.horizontalSlider_2.setMaximumSize(QSize(200, 16777215))
        self.horizontalSlider_2.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_2.addWidget(self.horizontalSlider_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.horizontalLayout_5.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.prevBtn = QPushButton(Dialog)
        self.prevBtn.setObjectName(u"prevBtn")

        self.horizontalLayout.addWidget(self.prevBtn)

        self.imgLab = QLabel(Dialog)
        self.imgLab.setObjectName(u"imgLab")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.imgLab.sizePolicy().hasHeightForWidth())
        self.imgLab.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.imgLab)

        self.nextBtn = QPushButton(Dialog)
        self.nextBtn.setObjectName(u"nextBtn")
        sizePolicy1.setHeightForWidth(self.nextBtn.sizePolicy().hasHeightForWidth())
        self.nextBtn.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.nextBtn)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u56fe\u7247\u8be6\u60c5", None))
        self.infoLab.setText(QCoreApplication.translate("Dialog", u"11", None))
        self.deleteBtn.setText(QCoreApplication.translate("Dialog", u"\u5220\u9664", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u4eae\u5ea6\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u5bf9\u6bd4\u5ea6\uff1a", None))
        self.prevBtn.setText(QCoreApplication.translate("Dialog", u"\u25c0", None))
        self.imgLab.setText("")
        self.nextBtn.setText(QCoreApplication.translate("Dialog", u"\u25b6", None))
    # retranslateUi

