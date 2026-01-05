# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createPjtUI.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGraphicsView,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(573, 385)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupProjectBasic = QGroupBox(Dialog)
        self.groupProjectBasic.setObjectName(u"groupProjectBasic")
        self.gridLayout_basic = QGridLayout(self.groupProjectBasic)
        self.gridLayout_basic.setObjectName(u"gridLayout_basic")
        self.groupMaskPreview = QGroupBox(self.groupProjectBasic)
        self.groupMaskPreview.setObjectName(u"groupMaskPreview")
        self.verticalLayout_maskPrev = QVBoxLayout(self.groupMaskPreview)
        self.verticalLayout_maskPrev.setObjectName(u"verticalLayout_maskPrev")
        self.maskPreview = QGraphicsView(self.groupMaskPreview)
        self.maskPreview.setObjectName(u"maskPreview")
        self.maskPreview.setMinimumSize(QSize(245, 134))

        self.verticalLayout_maskPrev.addWidget(self.maskPreview)


        self.gridLayout_basic.addWidget(self.groupMaskPreview, 3, 2, 1, 2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_10 = QLabel(self.groupProjectBasic)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_2.addWidget(self.label_10)

        self.pjtNameEdit = QLineEdit(self.groupProjectBasic)
        self.pjtNameEdit.setObjectName(u"pjtNameEdit")
        self.pjtNameEdit.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_2.addWidget(self.pjtNameEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.gridLayout_basic.addLayout(self.horizontalLayout_2, 0, 0, 1, 4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_11 = QLabel(self.groupProjectBasic)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_3.addWidget(self.label_11)

        self.pjtTypeCbx = QComboBox(self.groupProjectBasic)
        self.pjtTypeCbx.setObjectName(u"pjtTypeCbx")
        self.pjtTypeCbx.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_3.addWidget(self.pjtTypeCbx)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.gridLayout_basic.addLayout(self.horizontalLayout_3, 1, 0, 1, 4)

        self.lblMaskTitle = QLabel(self.groupProjectBasic)
        self.lblMaskTitle.setObjectName(u"lblMaskTitle")

        self.gridLayout_basic.addWidget(self.lblMaskTitle, 2, 2, 1, 1)

        self.groupTemplatePreview = QGroupBox(self.groupProjectBasic)
        self.groupTemplatePreview.setObjectName(u"groupTemplatePreview")
        self.verticalLayout_tmplPrev = QVBoxLayout(self.groupTemplatePreview)
        self.verticalLayout_tmplPrev.setObjectName(u"verticalLayout_tmplPrev")
        self.templatePreview = QGraphicsView(self.groupTemplatePreview)
        self.templatePreview.setObjectName(u"templatePreview")
        self.templatePreview.setMinimumSize(QSize(244, 134))

        self.verticalLayout_tmplPrev.addWidget(self.templatePreview)


        self.gridLayout_basic.addWidget(self.groupTemplatePreview, 3, 0, 1, 2)

        self.lblTemplateTitle = QLabel(self.groupProjectBasic)
        self.lblTemplateTitle.setObjectName(u"lblTemplateTitle")

        self.gridLayout_basic.addWidget(self.lblTemplateTitle, 2, 0, 1, 1)

        self.templateFileBtn = QToolButton(self.groupProjectBasic)
        self.templateFileBtn.setObjectName(u"templateFileBtn")

        self.gridLayout_basic.addWidget(self.templateFileBtn, 4, 1, 1, 1)

        self.maskFileBtn = QToolButton(self.groupProjectBasic)
        self.maskFileBtn.setObjectName(u"maskFileBtn")

        self.gridLayout_basic.addWidget(self.maskFileBtn, 4, 3, 1, 1)


        self.verticalLayout_2.addWidget(self.groupProjectBasic)

        self.verticalSpacer_2 = QSpacerItem(20, 77, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.confirmBtn = QPushButton(Dialog)
        self.confirmBtn.setObjectName(u"confirmBtn")
        self.confirmBtn.setMinimumSize(QSize(0, 35))

        self.horizontalLayout.addWidget(self.confirmBtn)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.cancelBtn = QPushButton(Dialog)
        self.cancelBtn.setObjectName(u"cancelBtn")
        self.cancelBtn.setMinimumSize(QSize(0, 35))

        self.horizontalLayout.addWidget(self.cancelBtn)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u65b0\u5efa\u9879\u76ee", None))
        self.groupProjectBasic.setTitle(QCoreApplication.translate("Dialog", u"\u9879\u76ee\u4fe1\u606f", None))
        self.groupMaskPreview.setTitle("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"\u9879\u76ee\u540d\uff1a", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"\u9879\u76ee\u7c7b\u578b\uff1a", None))
        self.lblMaskTitle.setText(QCoreApplication.translate("Dialog", u"Mask\u56fe\u50cf:", None))
        self.groupTemplatePreview.setTitle("")
        self.lblTemplateTitle.setText(QCoreApplication.translate("Dialog", u"\u6a21\u677f\u56fe\u50cf:", None))
        self.templateFileBtn.setText(QCoreApplication.translate("Dialog", u"\u5bfc\u5165\u2026", None))
        self.maskFileBtn.setText(QCoreApplication.translate("Dialog", u"\u5bfc\u5165\u2026", None))
        self.confirmBtn.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
        self.cancelBtn.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

