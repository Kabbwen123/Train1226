# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trainUI.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLayout, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QSplitter,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1179, 740)
        Form.setStyleSheet(u"")
        self.horizontalLayout_3 = QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_side = QVBoxLayout()
        self.verticalLayout_side.setSpacing(8)
        self.verticalLayout_side.setObjectName(u"verticalLayout_side")
        self.verticalLayout_side.setContentsMargins(0, 0, 0, 0)
        self.pjtInfoFrame = QFrame(Form)
        self.pjtInfoFrame.setObjectName(u"pjtInfoFrame")
        self.pjtInfoFrame.setMinimumSize(QSize(0, 0))
        self.pjtInfoFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.pjtInfoFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.pjtInfoFrame.setLineWidth(1)
        self.verticalLayout_2 = QVBoxLayout(self.pjtInfoFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout_side.addWidget(self.pjtInfoFrame)

        self.gbRuns = QGroupBox(Form)
        self.gbRuns.setObjectName(u"gbRuns")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbRuns.sizePolicy().hasHeightForWidth())
        self.gbRuns.setSizePolicy(sizePolicy)
        self.verticalLayout_runs = QVBoxLayout(self.gbRuns)
        self.verticalLayout_runs.setSpacing(8)
        self.verticalLayout_runs.setObjectName(u"verticalLayout_runs")
        self.verticalLayout_runs.setContentsMargins(10, 10, 10, 10)
        self.btnCreateModel = QPushButton(self.gbRuns)
        self.btnCreateModel.setObjectName(u"btnCreateModel")

        self.verticalLayout_runs.addWidget(self.btnCreateModel)

        self.scrollArea = QScrollArea(self.gbRuns)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setMinimumSize(QSize(320, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 318, 591))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_runs.addWidget(self.scrollArea)

        self.sideBottomBar = QFrame(self.gbRuns)
        self.sideBottomBar.setObjectName(u"sideBottomBar")
        self.sideBottomBar.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_sideBottom = QHBoxLayout(self.sideBottomBar)
        self.horizontalLayout_sideBottom.setSpacing(8)
        self.horizontalLayout_sideBottom.setObjectName(u"horizontalLayout_sideBottom")
        self.horizontalLayout_sideBottom.setContentsMargins(0, 0, 0, 0)
        self.btnPlay = QToolButton(self.sideBottomBar)
        self.btnPlay.setObjectName(u"btnPlay")

        self.horizontalLayout_sideBottom.addWidget(self.btnPlay)

        self.btnAssess = QToolButton(self.sideBottomBar)
        self.btnAssess.setObjectName(u"btnAssess")

        self.horizontalLayout_sideBottom.addWidget(self.btnAssess)


        self.verticalLayout_runs.addWidget(self.sideBottomBar)


        self.verticalLayout_side.addWidget(self.gbRuns)


        self.horizontalLayout_3.addLayout(self.verticalLayout_side)

        self.verticalLayout_main_2 = QVBoxLayout()
        self.verticalLayout_main_2.setSpacing(8)
        self.verticalLayout_main_2.setObjectName(u"verticalLayout_main_2")
        self.verticalLayout_main_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, -1, -1, -1)
        self.mutedHint_3 = QLabel(Form)
        self.mutedHint_3.setObjectName(u"mutedHint_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.mutedHint_3.sizePolicy().hasHeightForWidth())
        self.mutedHint_3.setSizePolicy(sizePolicy2)
        self.mutedHint_3.setMinimumSize(QSize(0, 50))
        self.mutedHint_3.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout.addWidget(self.mutedHint_3)

        self.saveCfgBtn = QPushButton(Form)
        self.saveCfgBtn.setObjectName(u"saveCfgBtn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.saveCfgBtn.sizePolicy().hasHeightForWidth())
        self.saveCfgBtn.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.saveCfgBtn)


        self.verticalLayout_main_2.addLayout(self.horizontalLayout)

        self.splitter_panels_2 = QSplitter(Form)
        self.splitter_panels_2.setObjectName(u"splitter_panels_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.splitter_panels_2.sizePolicy().hasHeightForWidth())
        self.splitter_panels_2.setSizePolicy(sizePolicy4)
        self.splitter_panels_2.setOrientation(Qt.Orientation.Horizontal)
        self.colLeft_2 = QWidget(self.splitter_panels_2)
        self.colLeft_2.setObjectName(u"colLeft_2")
        self.verticalLayout_colLeft_2 = QVBoxLayout(self.colLeft_2)
        self.verticalLayout_colLeft_2.setSpacing(8)
        self.verticalLayout_colLeft_2.setObjectName(u"verticalLayout_colLeft_2")
        self.verticalLayout_colLeft_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_colLeft_2.setContentsMargins(0, 0, 0, 0)
        self.gbSplit_3 = QGroupBox(self.colLeft_2)
        self.gbSplit_3.setObjectName(u"gbSplit_3")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.gbSplit_3.sizePolicy().hasHeightForWidth())
        self.gbSplit_3.setSizePolicy(sizePolicy5)
        self.gbSplit_3.setMinimumSize(QSize(400, 0))
        self.gridLayout_4 = QGridLayout(self.gbSplit_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")

        self.verticalLayout_colLeft_2.addWidget(self.gbSplit_3)

        self.gbNetwork_2 = QGroupBox(self.colLeft_2)
        self.gbNetwork_2.setObjectName(u"gbNetwork_2")
        sizePolicy5.setHeightForWidth(self.gbNetwork_2.sizePolicy().hasHeightForWidth())
        self.gbNetwork_2.setSizePolicy(sizePolicy5)
        self.gbNetwork_2.setMinimumSize(QSize(400, 0))
        self.gridLayout_network_2 = QGridLayout(self.gbNetwork_2)
        self.gridLayout_network_2.setObjectName(u"gridLayout_network_2")
        self.gridLayout_network_2.setHorizontalSpacing(8)
        self.gridLayout_network_2.setVerticalSpacing(6)
        self.gridLayout_network_2.setContentsMargins(10, 10, 10, 10)
        self.backbone_nameLab = QLabel(self.gbNetwork_2)
        self.backbone_nameLab.setObjectName(u"backbone_nameLab")

        self.gridLayout_network_2.addWidget(self.backbone_nameLab, 0, 0, 1, 1)

        self.input_sizeWSpb = QSpinBox(self.gbNetwork_2)
        self.input_sizeWSpb.setObjectName(u"input_sizeWSpb")
        self.input_sizeWSpb.setMaximum(1920)
        self.input_sizeWSpb.setValue(256)

        self.gridLayout_network_2.addWidget(self.input_sizeWSpb, 1, 1, 1, 1)

        self.input_sizeWLab = QLabel(self.gbNetwork_2)
        self.input_sizeWLab.setObjectName(u"input_sizeWLab")

        self.gridLayout_network_2.addWidget(self.input_sizeWLab, 1, 0, 1, 1)

        self.patch_sizeSpb = QSpinBox(self.gbNetwork_2)
        self.patch_sizeSpb.setObjectName(u"patch_sizeSpb")
        self.patch_sizeSpb.setMaximum(1024)
        self.patch_sizeSpb.setSingleStep(2)
        self.patch_sizeSpb.setValue(33)

        self.gridLayout_network_2.addWidget(self.patch_sizeSpb, 3, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(3, 4, -1, -1)
        self.embedding1Cbx = QCheckBox(self.gbNetwork_2)
        self.embedding1Cbx.setObjectName(u"embedding1Cbx")
        self.embedding1Cbx.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"    border: 1px solid #FFFFFF;\n"
"    background: #FFFFFF;         /* \u65b9\u6846\u767d */\n"
"    border-radius: 3px;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: #2B2B2B;         /* \u53cd\u8272\uff1a\u9009\u4e2d\u53d8\u6df1\u5e95 */\n"
"    border: 1px solid #FFFFFF;\n"
"    image: url(:/icons/check_white.svg);  /* \u767d\u52fe */\n"
"}\n"
"QCheckBox::indicator:checked:hover {\n"
"    background: #3A3A3A;\n"
"}")

        self.horizontalLayout_2.addWidget(self.embedding1Cbx)

        self.embedding2Cbx = QCheckBox(self.gbNetwork_2)
        self.embedding2Cbx.setObjectName(u"embedding2Cbx")
        self.embedding2Cbx.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"    border: 1px solid #FFFFFF;\n"
"    background: #FFFFFF;         /* \u65b9\u6846\u767d */\n"
"    border-radius: 3px;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: #2B2B2B;         /* \u53cd\u8272\uff1a\u9009\u4e2d\u53d8\u6df1\u5e95 */\n"
"    border: 1px solid #FFFFFF;\n"
"    image: url(:/icons/check_white.svg);  /* \u767d\u52fe */\n"
"}\n"
"QCheckBox::indicator:checked:hover {\n"
"    background: #3A3A3A;\n"
"}")

        self.horizontalLayout_2.addWidget(self.embedding2Cbx)

        self.embedding3Cbx = QCheckBox(self.gbNetwork_2)
        self.embedding3Cbx.setObjectName(u"embedding3Cbx")
        self.embedding3Cbx.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"    border: 1px solid #FFFFFF;\n"
"    background: #FFFFFF;         /* \u65b9\u6846\u767d */\n"
"    border-radius: 3px;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: #2B2B2B;         /* \u53cd\u8272\uff1a\u9009\u4e2d\u53d8\u6df1\u5e95 */\n"
"    border: 1px solid #FFFFFF;\n"
"    image: url(:/icons/check_white.svg);  /* \u767d\u52fe */\n"
"}\n"
"QCheckBox::indicator:checked:hover {\n"
"    background: #3A3A3A;\n"
"}")

        self.horizontalLayout_2.addWidget(self.embedding3Cbx)

        self.embedding4Cbx = QCheckBox(self.gbNetwork_2)
        self.embedding4Cbx.setObjectName(u"embedding4Cbx")
        self.embedding4Cbx.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"    border: 1px solid #FFFFFF;\n"
"    background: #FFFFFF;         /* \u65b9\u6846\u767d */\n"
"    border-radius: 3px;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: #2B2B2B;         /* \u53cd\u8272\uff1a\u9009\u4e2d\u53d8\u6df1\u5e95 */\n"
"    border: 1px solid #FFFFFF;\n"
"    image: url(:/icons/check_white.svg);  /* \u767d\u52fe */\n"
"}\n"
"QCheckBox::indicator:checked:hover {\n"
"    background: #3A3A3A;\n"
"}")

        self.horizontalLayout_2.addWidget(self.embedding4Cbx)


        self.gridLayout_network_2.addLayout(self.horizontalLayout_2, 4, 1, 1, 1)

        self.patch_sizeLab = QLabel(self.gbNetwork_2)
        self.patch_sizeLab.setObjectName(u"patch_sizeLab")

        self.gridLayout_network_2.addWidget(self.patch_sizeLab, 3, 0, 1, 1)

        self.backbone_nameCmb = QComboBox(self.gbNetwork_2)
        self.backbone_nameCmb.addItem("")
        self.backbone_nameCmb.addItem("")
        self.backbone_nameCmb.addItem("")
        self.backbone_nameCmb.addItem("")
        self.backbone_nameCmb.setObjectName(u"backbone_nameCmb")

        self.gridLayout_network_2.addWidget(self.backbone_nameCmb, 0, 1, 1, 1)

        self.input_sizeHSpb = QSpinBox(self.gbNetwork_2)
        self.input_sizeHSpb.setObjectName(u"input_sizeHSpb")
        self.input_sizeHSpb.setMaximum(1920)
        self.input_sizeHSpb.setValue(256)

        self.gridLayout_network_2.addWidget(self.input_sizeHSpb, 2, 1, 1, 1)

        self.input_sizeHLab = QLabel(self.gbNetwork_2)
        self.input_sizeHLab.setObjectName(u"input_sizeHLab")

        self.gridLayout_network_2.addWidget(self.input_sizeHLab, 2, 0, 1, 1)

        self.embeddingLab = QLabel(self.gbNetwork_2)
        self.embeddingLab.setObjectName(u"embeddingLab")

        self.gridLayout_network_2.addWidget(self.embeddingLab, 4, 0, 1, 1)


        self.verticalLayout_colLeft_2.addWidget(self.gbNetwork_2)

        self.spacer_colLeft_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_colLeft_2.addItem(self.spacer_colLeft_2)

        self.splitter_panels_2.addWidget(self.colLeft_2)
        self.colMiddle_2 = QWidget(self.splitter_panels_2)
        self.colMiddle_2.setObjectName(u"colMiddle_2")
        self.verticalLayout_colMiddle_2 = QVBoxLayout(self.colMiddle_2)
        self.verticalLayout_colMiddle_2.setSpacing(8)
        self.verticalLayout_colMiddle_2.setObjectName(u"verticalLayout_colMiddle_2")
        self.verticalLayout_colMiddle_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_colMiddle_2.setContentsMargins(0, 0, 0, 0)
        self.gbDevice_2 = QGroupBox(self.colMiddle_2)
        self.gbDevice_2.setObjectName(u"gbDevice_2")
        sizePolicy5.setHeightForWidth(self.gbDevice_2.sizePolicy().hasHeightForWidth())
        self.gbDevice_2.setSizePolicy(sizePolicy5)
        self.gbDevice_2.setMinimumSize(QSize(400, 0))
        self.gridLayout_device_2 = QGridLayout(self.gbDevice_2)
        self.gridLayout_device_2.setObjectName(u"gridLayout_device_2")
        self.gridLayout_device_2.setHorizontalSpacing(8)
        self.gridLayout_device_2.setVerticalSpacing(6)
        self.gridLayout_device_2.setContentsMargins(10, 10, 10, 10)
        self.deviceLab = QLabel(self.gbDevice_2)
        self.deviceLab.setObjectName(u"deviceLab")

        self.gridLayout_device_2.addWidget(self.deviceLab, 0, 0, 1, 1)

        self.deviceCbx = QComboBox(self.gbDevice_2)
        self.deviceCbx.setObjectName(u"deviceCbx")

        self.gridLayout_device_2.addWidget(self.deviceCbx, 0, 1, 1, 1)


        self.verticalLayout_colMiddle_2.addWidget(self.gbDevice_2)

        self.gbTrainParams_3 = QGroupBox(self.colMiddle_2)
        self.gbTrainParams_3.setObjectName(u"gbTrainParams_3")
        sizePolicy5.setHeightForWidth(self.gbTrainParams_3.sizePolicy().hasHeightForWidth())
        self.gbTrainParams_3.setSizePolicy(sizePolicy5)
        self.gbTrainParams_3.setMinimumSize(QSize(400, 0))
        self.verticalLayout_trainParams_advanced = QVBoxLayout(self.gbTrainParams_3)
        self.verticalLayout_trainParams_advanced.setSpacing(8)
        self.verticalLayout_trainParams_advanced.setObjectName(u"verticalLayout_trainParams_advanced")
        self.verticalLayout_trainParams_advanced.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_network_4 = QGridLayout()
        self.gridLayout_network_4.setObjectName(u"gridLayout_network_4")
        self.gridLayout_network_4.setHorizontalSpacing(8)
        self.gridLayout_network_4.setVerticalSpacing(6)
        self.batch_sizeLab = QLabel(self.gbTrainParams_3)
        self.batch_sizeLab.setObjectName(u"batch_sizeLab")

        self.gridLayout_network_4.addWidget(self.batch_sizeLab, 0, 0, 1, 1)

        self.batch_sizeCmb = QComboBox(self.gbTrainParams_3)
        self.batch_sizeCmb.addItem("")
        self.batch_sizeCmb.addItem("")
        self.batch_sizeCmb.addItem("")
        self.batch_sizeCmb.addItem("")
        self.batch_sizeCmb.addItem("")
        self.batch_sizeCmb.addItem("")
        self.batch_sizeCmb.setObjectName(u"batch_sizeCmb")

        self.gridLayout_network_4.addWidget(self.batch_sizeCmb, 0, 1, 1, 1)

        self.seedLab = QLabel(self.gbTrainParams_3)
        self.seedLab.setObjectName(u"seedLab")

        self.gridLayout_network_4.addWidget(self.seedLab, 1, 0, 1, 1)

        self.seedSpb = QSpinBox(self.gbTrainParams_3)
        self.seedSpb.setObjectName(u"seedSpb")
        self.seedSpb.setMinimumSize(QSize(0, 0))
        self.seedSpb.setMinimum(1)
        self.seedSpb.setMaximum(999999999)
        self.seedSpb.setValue(70000)

        self.gridLayout_network_4.addWidget(self.seedSpb, 1, 1, 1, 1)

        self.max_train_featuresLab = QLabel(self.gbTrainParams_3)
        self.max_train_featuresLab.setObjectName(u"max_train_featuresLab")

        self.gridLayout_network_4.addWidget(self.max_train_featuresLab, 2, 0, 1, 1)

        self.max_train_featuresSpb = QSpinBox(self.gbTrainParams_3)
        self.max_train_featuresSpb.setObjectName(u"max_train_featuresSpb")
        self.max_train_featuresSpb.setMinimumSize(QSize(0, 0))
        self.max_train_featuresSpb.setMinimum(1000)
        self.max_train_featuresSpb.setMaximum(999999999)
        self.max_train_featuresSpb.setValue(3333)

        self.gridLayout_network_4.addWidget(self.max_train_featuresSpb, 2, 1, 1, 1)


        self.verticalLayout_trainParams_advanced.addLayout(self.gridLayout_network_4)

        self.btnAdvancedTrainParams = QToolButton(self.gbTrainParams_3)
        self.btnAdvancedTrainParams.setObjectName(u"btnAdvancedTrainParams")
        self.btnAdvancedTrainParams.setCheckable(True)
        self.btnAdvancedTrainParams.setChecked(False)
        self.btnAdvancedTrainParams.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.btnAdvancedTrainParams.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnAdvancedTrainParams.setAutoRaise(True)
        self.btnAdvancedTrainParams.setArrowType(Qt.ArrowType.DownArrow)

        self.verticalLayout_trainParams_advanced.addWidget(self.btnAdvancedTrainParams)

        self.widget = QWidget(self.gbTrainParams_3)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.neighborsCmb = QComboBox(self.widget)
        self.neighborsCmb.addItem("")
        self.neighborsCmb.addItem("")
        self.neighborsCmb.addItem("")
        self.neighborsCmb.setObjectName(u"neighborsCmb")

        self.gridLayout.addWidget(self.neighborsCmb, 3, 1, 1, 1)

        self.coresetCmb = QComboBox(self.widget)
        self.coresetCmb.addItem("")
        self.coresetCmb.addItem("")
        self.coresetCmb.setObjectName(u"coresetCmb")

        self.gridLayout.addWidget(self.coresetCmb, 2, 1, 1, 1)

        self.neighborsLab = QLabel(self.widget)
        self.neighborsLab.setObjectName(u"neighborsLab")

        self.gridLayout.addWidget(self.neighborsLab, 3, 0, 1, 1)

        self.faissLab = QLabel(self.widget)
        self.faissLab.setObjectName(u"faissLab")

        self.gridLayout.addWidget(self.faissLab, 0, 0, 1, 1)

        self.faissCmb = QComboBox(self.widget)
        self.faissCmb.addItem("")
        self.faissCmb.addItem("")
        self.faissCmb.addItem("")
        self.faissCmb.addItem("")
        self.faissCmb.setObjectName(u"faissCmb")

        self.gridLayout.addWidget(self.faissCmb, 0, 1, 1, 1)

        self.coresetLab = QLabel(self.widget)
        self.coresetLab.setObjectName(u"coresetLab")

        self.gridLayout.addWidget(self.coresetLab, 2, 0, 1, 1)

        self.faissWidget = QWidget(self.widget)
        self.faissWidget.setObjectName(u"faissWidget")
        self.formLayout = QFormLayout(self.faissWidget)
        self.formLayout.setObjectName(u"formLayout")

        self.gridLayout.addWidget(self.faissWidget, 1, 0, 1, 2)


        self.verticalLayout_trainParams_advanced.addWidget(self.widget)


        self.verticalLayout_colMiddle_2.addWidget(self.gbTrainParams_3)

        self.spacer_colMiddle_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_colMiddle_2.addItem(self.spacer_colMiddle_2)

        self.splitter_panels_2.addWidget(self.colMiddle_2)

        self.verticalLayout_main_2.addWidget(self.splitter_panels_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_main_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.gbRuns.setTitle(QCoreApplication.translate("Form", u"\u6a21\u578b\u8bad\u7ec3", None))
        self.btnCreateModel.setText(QCoreApplication.translate("Form", u"\u521b\u5efa\u6a21\u578b", None))
        self.btnPlay.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u8bad\u7ec3", None))
        self.btnAssess.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u8bc4\u4f30", None))
        self.mutedHint_3.setText(QCoreApplication.translate("Form", u"\u8bad\u7ec3\u5f00\u59cb\u540e\u5373\u65e0\u6cd5\u66f4\u6539\u8bad\u7ec3\u53c2\u6570\u3002\u521b\u5efa\u65b0\u8bad\u7ec3\u6216\u91cd\u7f6e\u8bad\u7ec3\u3002", None))
        self.saveCfgBtn.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u914d\u7f6e", None))
        self.gbSplit_3.setTitle(QCoreApplication.translate("Form", u"\u6570\u636e\u96c6", None))
        self.gbNetwork_2.setTitle(QCoreApplication.translate("Form", u"\u795e\u7ecf\u7f51\u7edc", None))
        self.backbone_nameLab.setText(QCoreApplication.translate("Form", u"\u9884\u8bad\u7ec3\u6a21\u578b", None))
        self.input_sizeWLab.setText(QCoreApplication.translate("Form", u"\u56fe\u50cf\u5bbd\u5ea6", None))
        self.embedding1Cbx.setText(QCoreApplication.translate("Form", u"1", None))
        self.embedding2Cbx.setText(QCoreApplication.translate("Form", u"2", None))
        self.embedding3Cbx.setText(QCoreApplication.translate("Form", u"3", None))
        self.embedding4Cbx.setText(QCoreApplication.translate("Form", u"4", None))
        self.patch_sizeLab.setText(QCoreApplication.translate("Form", u"\u8865\u4e01\u5927\u5c0f", None))
        self.backbone_nameCmb.setItemText(0, QCoreApplication.translate("Form", u"resnet18", None))
        self.backbone_nameCmb.setItemText(1, QCoreApplication.translate("Form", u"resnet34", None))
        self.backbone_nameCmb.setItemText(2, QCoreApplication.translate("Form", u"resnet50", None))
        self.backbone_nameCmb.setItemText(3, QCoreApplication.translate("Form", u"wide_resnet50_2", None))

        self.input_sizeHLab.setText(QCoreApplication.translate("Form", u"\u56fe\u50cf\u9ad8\u5ea6", None))
        self.embeddingLab.setText(QCoreApplication.translate("Form", u"\u8bad\u7ec3\u5c42", None))
        self.gbDevice_2.setTitle(QCoreApplication.translate("Form", u"\u914d\u7f6e", None))
        self.deviceLab.setText(QCoreApplication.translate("Form", u"\u8bbe\u5907", None))
#if QT_CONFIG(tooltip)
        self.gbTrainParams_3.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.gbTrainParams_3.setTitle(QCoreApplication.translate("Form", u"\u8bad\u7ec3\u53c2\u6570", None))
        self.batch_sizeLab.setText(QCoreApplication.translate("Form", u"\u6279\u5927\u5c0f", None))
        self.batch_sizeCmb.setItemText(0, QCoreApplication.translate("Form", u"2", None))
        self.batch_sizeCmb.setItemText(1, QCoreApplication.translate("Form", u"4", None))
        self.batch_sizeCmb.setItemText(2, QCoreApplication.translate("Form", u"8", None))
        self.batch_sizeCmb.setItemText(3, QCoreApplication.translate("Form", u"16", None))
        self.batch_sizeCmb.setItemText(4, QCoreApplication.translate("Form", u"32", None))
        self.batch_sizeCmb.setItemText(5, QCoreApplication.translate("Form", u"64", None))

        self.seedLab.setText(QCoreApplication.translate("Form", u"\u968f\u673a\u79cd\u5b50", None))
#if QT_CONFIG(tooltip)
        self.max_train_featuresLab.setToolTip(QCoreApplication.translate("Form", u"\u6570\u503c\u8d8a\u5927\uff0c\u540e\u9762\u63a8\u7406\u7684\u6548\u7387\u53ef\u80fd\u6709\u6240\u5f71\u54cd", None))
#endif // QT_CONFIG(tooltip)
        self.max_train_featuresLab.setText(QCoreApplication.translate("Form", u"\u7279\u5f81\u5e93\u6700\u5927\u5bb9\u91cf", None))
#if QT_CONFIG(tooltip)
        self.max_train_featuresSpb.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btnAdvancedTrainParams.setText(QCoreApplication.translate("Form", u"\u9ad8\u7ea7\u8bbe\u7f6e", None))
        self.neighborsCmb.setItemText(0, QCoreApplication.translate("Form", u"5", None))
        self.neighborsCmb.setItemText(1, QCoreApplication.translate("Form", u"7", None))
        self.neighborsCmb.setItemText(2, QCoreApplication.translate("Form", u"9", None))

        self.coresetCmb.setItemText(0, QCoreApplication.translate("Form", u"random", None))
        self.coresetCmb.setItemText(1, QCoreApplication.translate("Form", u"kcenter", None))

        self.neighborsLab.setText(QCoreApplication.translate("Form", u"\u6700\u90bb\u8fd1\u6570\u91cf", None))
        self.faissLab.setText(QCoreApplication.translate("Form", u"\u68c0\u7d22\u65b9\u5f0f", None))
        self.faissCmb.setItemText(0, QCoreApplication.translate("Form", u"Flat", None))
        self.faissCmb.setItemText(1, QCoreApplication.translate("Form", u"IVFFlat", None))
        self.faissCmb.setItemText(2, QCoreApplication.translate("Form", u"IVFPQ", None))
        self.faissCmb.setItemText(3, QCoreApplication.translate("Form", u"HNSW", None))

        self.coresetLab.setText(QCoreApplication.translate("Form", u"\u7cbe\u7b80\u7b56\u7565", None))
    # retranslateUi

