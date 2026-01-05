# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'assessmentUI.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1263, 615)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pieGroupBox = QGroupBox(Dialog)
        self.pieGroupBox.setObjectName(u"pieGroupBox")
        self.verticalLayout_3 = QVBoxLayout(self.pieGroupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.pieGroupBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label)

        self.f1Lab = QLabel(self.pieGroupBox)
        self.f1Lab.setObjectName(u"f1Lab")
        self.f1Lab.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.f1Lab)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.pieOkNgHost = QWidget(self.pieGroupBox)
        self.pieOkNgHost.setObjectName(u"pieOkNgHost")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pieOkNgHost.sizePolicy().hasHeightForWidth())
        self.pieOkNgHost.setSizePolicy(sizePolicy)
        self.pieOkNgHost.setMinimumSize(QSize(280, 0))

        self.verticalLayout_3.addWidget(self.pieOkNgHost)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout_6.setContentsMargins(0, -1, -1, -1)
        self.label_9 = QLabel(self.pieGroupBox)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_6.addWidget(self.label_9)

        self.detectTimeLab = QLabel(self.pieGroupBox)
        self.detectTimeLab.setObjectName(u"detectTimeLab")
        self.detectTimeLab.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.detectTimeLab)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.label_3 = QLabel(self.pieGroupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_9.addWidget(self.label_3)

        self.sumImgLab = QLabel(self.pieGroupBox)
        self.sumImgLab.setObjectName(u"sumImgLab")
        self.sumImgLab.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.sumImgLab)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.label_8 = QLabel(self.pieGroupBox)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_10.addWidget(self.label_8)

        self.costTimeLab = QLabel(self.pieGroupBox)
        self.costTimeLab.setObjectName(u"costTimeLab")
        self.costTimeLab.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.costTimeLab)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)


        self.horizontalLayout_8.addWidget(self.pieGroupBox)

        self.scoreGroupBox = QGroupBox(Dialog)
        self.scoreGroupBox.setObjectName(u"scoreGroupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scoreGroupBox.sizePolicy().hasHeightForWidth())
        self.scoreGroupBox.setSizePolicy(sizePolicy1)
        self.verticalLayout_score = QVBoxLayout(self.scoreGroupBox)
        self.verticalLayout_score.setObjectName(u"verticalLayout_score")
        self.verticalLayout_score.setContentsMargins(10, 10, 10, 10)
        self.scoreChartHost = QWidget(self.scoreGroupBox)
        self.scoreChartHost.setObjectName(u"scoreChartHost")
        self.scoreChartHost.setMinimumSize(QSize(700, 250))

        self.verticalLayout_score.addWidget(self.scoreChartHost)


        self.horizontalLayout_8.addWidget(self.scoreGroupBox)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.cmGroupBox = QGroupBox(Dialog)
        self.cmGroupBox.setObjectName(u"cmGroupBox")
        self.cmGroupBox.setMinimumSize(QSize(200, 249))
        self.cmGroupBox.setMaximumSize(QSize(200, 300))
        self.cmGroupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_cm = QVBoxLayout(self.cmGroupBox)
        self.verticalLayout_cm.setObjectName(u"verticalLayout_cm")
        self.verticalLayout_cm.setContentsMargins(10, 40, 10, 40)

        self.horizontalLayout_5.addWidget(self.cmGroupBox)

        self.imageGroupBox = QGroupBox(Dialog)
        self.imageGroupBox.setObjectName(u"imageGroupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.imageGroupBox.sizePolicy().hasHeightForWidth())
        self.imageGroupBox.setSizePolicy(sizePolicy2)
        self.imageGroupBox.setMaximumSize(QSize(16777215, 300))

        self.horizontalLayout_5.addWidget(self.imageGroupBox)

        self.detailGroupBox = QGroupBox(Dialog)
        self.detailGroupBox.setObjectName(u"detailGroupBox")
        self.detailGroupBox.setMinimumSize(QSize(200, 300))
        self.detailGroupBox.setMaximumSize(QSize(200, 300))
        self.formLayout = QFormLayout(self.detailGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.lblNameTitle = QLabel(self.detailGroupBox)
        self.lblNameTitle.setObjectName(u"lblNameTitle")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblNameTitle)

        self.lblImageName = QLabel(self.detailGroupBox)
        self.lblImageName.setObjectName(u"lblImageName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lblImageName)

        self.lblGtTitle = QLabel(self.detailGroupBox)
        self.lblGtTitle.setObjectName(u"lblGtTitle")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblGtTitle)

        self.tagLab = QLabel(self.detailGroupBox)
        self.tagLab.setObjectName(u"tagLab")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.tagLab)

        self.lblPredTitle = QLabel(self.detailGroupBox)
        self.lblPredTitle.setObjectName(u"lblPredTitle")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblPredTitle)

        self.lblPredValue = QLabel(self.detailGroupBox)
        self.lblPredValue.setObjectName(u"lblPredValue")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lblPredValue)

        self.lblScoreTitle = QLabel(self.detailGroupBox)
        self.lblScoreTitle.setObjectName(u"lblScoreTitle")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblScoreTitle)

        self.lblScoreValue = QLabel(self.detailGroupBox)
        self.lblScoreValue.setObjectName(u"lblScoreValue")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lblScoreValue)

        self.lblStatusTitle = QLabel(self.detailGroupBox)
        self.lblStatusTitle.setObjectName(u"lblStatusTitle")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lblStatusTitle)

        self.lblStatusValue = QLabel(self.detailGroupBox)
        self.lblStatusValue.setObjectName(u"lblStatusValue")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.lblStatusValue)


        self.horizontalLayout_5.addWidget(self.detailGroupBox)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pieGroupBox.setTitle(QCoreApplication.translate("Dialog", u"\u7efc\u5408\u6307\u6807", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"F1\u5206\u6570:", None))
        self.f1Lab.setText(QCoreApplication.translate("Dialog", u"--%", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"\u5404\u56fe\u50cf\u7684\u63a8\u65ad\u65f6\u95f4\uff1a", None))
        self.detectTimeLab.setText(QCoreApplication.translate("Dialog", u"--ms", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u56fe\u50cf\u603b\u6570\uff1a", None))
        self.sumImgLab.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\u5df2\u7528\u65f6\u95f4\uff1a", None))
        self.costTimeLab.setText(QCoreApplication.translate("Dialog", u"--s", None))
        self.scoreGroupBox.setTitle(QCoreApplication.translate("Dialog", u"\u76f4\u65b9\u56fe\u5206\u6570", None))
        self.cmGroupBox.setTitle(QCoreApplication.translate("Dialog", u"\u6df7\u6dc6\u77e9\u9635", None))
        self.imageGroupBox.setTitle(QCoreApplication.translate("Dialog", u"\u56fe\u50cf", None))
        self.detailGroupBox.setTitle(QCoreApplication.translate("Dialog", u"\u56fe\u50cf\u8be6\u60c5", None))
        self.lblNameTitle.setText(QCoreApplication.translate("Dialog", u"\u56fe\u50cf\u540d\u79f0\uff1a", None))
        self.lblImageName.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.lblGtTitle.setText(QCoreApplication.translate("Dialog", u"\u6807\u7b7e\u7c7b\u522b", None))
        self.tagLab.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.lblPredTitle.setText(QCoreApplication.translate("Dialog", u"\u9884\u6d4b", None))
        self.lblPredValue.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.lblScoreTitle.setText(QCoreApplication.translate("Dialog", u"\u5206\u6570", None))
        self.lblScoreValue.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.lblStatusTitle.setText(QCoreApplication.translate("Dialog", u"\u9884\u6d4b\u72b6\u6001\uff1a", None))
        self.lblStatusValue.setText(QCoreApplication.translate("Dialog", u"-", None))
    # retranslateUi

