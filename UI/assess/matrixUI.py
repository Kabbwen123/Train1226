# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'matrixUI.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(247, 215)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        font = QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 0, 1, 1, 3)

        self.okGoodLab = QLabel(Form)
        self.okGoodLab.setObjectName(u"okGoodLab")
        self.okGoodLab.setMinimumSize(QSize(30, 30))
        font1 = QFont()
        font1.setPointSize(15)
        self.okGoodLab.setFont(font1)
        self.okGoodLab.setStyleSheet(u"background-color: rgb(0, 151, 136);\n"
"color: rgb(255, 255, 255);")
        self.okGoodLab.setFrameShape(QFrame.Shape.Box)
        self.okGoodLab.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.okGoodLab, 1, 1, 1, 1)

        self.ngGoodLab = QLabel(Form)
        self.ngGoodLab.setObjectName(u"ngGoodLab")
        self.ngGoodLab.setMinimumSize(QSize(30, 30))
        self.ngGoodLab.setFont(font1)
        self.ngGoodLab.setStyleSheet(u"background-color: rgb(132, 138, 138);\n"
"color: rgb(255, 255, 255);")
        self.ngGoodLab.setFrameShape(QFrame.Shape.Box)
        self.ngGoodLab.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.ngGoodLab, 1, 2, 1, 1)

        self.preOkSumLab = QLabel(Form)
        self.preOkSumLab.setObjectName(u"preOkSumLab")
        self.preOkSumLab.setMinimumSize(QSize(30, 30))
        self.preOkSumLab.setFont(font1)
        self.preOkSumLab.setStyleSheet(u"background-color: rgb(58, 56, 53);\n"
"color: rgb(255, 255, 255);")
        self.preOkSumLab.setFrameShape(QFrame.Shape.Box)
        self.preOkSumLab.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.preOkSumLab, 1, 3, 1, 1)

        self.label_14 = QLabel(Form)
        self.label_14.setObjectName(u"label_14")
        font2 = QFont()
        font2.setPointSize(15)
        font2.setBold(True)
        self.label_14.setFont(font2)
        self.label_14.setStyleSheet(u"color: rgb(0, 170, 0);")
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_14, 1, 4, 1, 1)

        self.okBadLab = QLabel(Form)
        self.okBadLab.setObjectName(u"okBadLab")
        self.okBadLab.setMinimumSize(QSize(30, 30))
        self.okBadLab.setFont(font1)
        self.okBadLab.setStyleSheet(u"background-color: rgb(132, 138, 138);\n"
"color: rgb(255, 255, 255);")
        self.okBadLab.setFrameShape(QFrame.Shape.Box)
        self.okBadLab.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.okBadLab, 2, 1, 1, 1)

        self.ngBadLab = QLabel(Form)
        self.ngBadLab.setObjectName(u"ngBadLab")
        self.ngBadLab.setMinimumSize(QSize(30, 30))
        self.ngBadLab.setFont(font1)
        self.ngBadLab.setStyleSheet(u"background-color: rgb(0, 151, 136);\n"
"color: rgb(255, 255, 255);")
        self.ngBadLab.setFrameShape(QFrame.Shape.Box)
        self.ngBadLab.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.ngBadLab, 2, 2, 1, 1)

        self.preNgSumLab = QLabel(Form)
        self.preNgSumLab.setObjectName(u"preNgSumLab")
        self.preNgSumLab.setMinimumSize(QSize(30, 30))
        self.preNgSumLab.setFont(font1)
        self.preNgSumLab.setStyleSheet(u"background-color: rgb(58, 56, 53);\n"
"color: rgb(255, 255, 255);")
        self.preNgSumLab.setFrameShape(QFrame.Shape.Box)
        self.preNgSumLab.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.preNgSumLab, 2, 3, 1, 1)

        self.label_16 = QLabel(Form)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font2)
        self.label_16.setStyleSheet(u"color: rgb(197, 66, 0);")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_16, 2, 4, 1, 1)

        self.okSumLab = QLabel(Form)
        self.okSumLab.setObjectName(u"okSumLab")
        self.okSumLab.setMinimumSize(QSize(30, 30))
        self.okSumLab.setFont(font1)
        self.okSumLab.setStyleSheet(u"background-color: rgb(58, 56, 53);\n"
"color: rgb(255, 255, 255);")
        self.okSumLab.setFrameShape(QFrame.Shape.Box)
        self.okSumLab.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.okSumLab, 3, 1, 1, 1)

        self.ngSumLab = QLabel(Form)
        self.ngSumLab.setObjectName(u"ngSumLab")
        self.ngSumLab.setMinimumSize(QSize(30, 30))
        self.ngSumLab.setFont(font1)
        self.ngSumLab.setStyleSheet(u"background-color: rgb(58, 56, 53);\n"
"color: rgb(255, 255, 255);")
        self.ngSumLab.setFrameShape(QFrame.Shape.Box)
        self.ngSumLab.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.ngSumLab, 3, 2, 1, 1)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)
        self.label_5.setStyleSheet(u"color: rgb(0, 170, 255);")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 4, 1, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font2)
        self.label_6.setStyleSheet(u"color: rgb(243, 194, 0);")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_6, 4, 2, 1, 1)

        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")
        font3 = QFont()
        font3.setPointSize(11)
        font3.setHintingPreference(QFont.PreferDefaultHinting)
        self.label_9.setFont(font3)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_9, 1, 0, 2, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u771f\u5b9e", None))
        self.okGoodLab.setText(QCoreApplication.translate("Form", u"0", None))
        self.ngGoodLab.setText(QCoreApplication.translate("Form", u"0", None))
        self.preOkSumLab.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"OK", None))
        self.okBadLab.setText(QCoreApplication.translate("Form", u"0", None))
        self.ngBadLab.setText(QCoreApplication.translate("Form", u"0", None))
        self.preNgSumLab.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"NG", None))
        self.okSumLab.setText(QCoreApplication.translate("Form", u"0", None))
        self.ngSumLab.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"OK", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"NG", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u9884\n"
"\u6d4b", None))
    # retranslateUi

