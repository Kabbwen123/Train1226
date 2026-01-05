from PySide6.QtCore import QEvent, Signal
from PySide6.QtWidgets import QWidget

from Interface.UI.assess.matrixUI import Ui_Form


class MatrixWidget(QWidget, Ui_Form):
    okGoodClicked = Signal()
    okBadClicked = Signal()
    ngGoodClicked = Signal()
    ngBadClicked = Signal()

    okSumClicked = Signal()
    ngSumClicked = Signal()
    preOkSumClicked = Signal()
    preNgSumClicked = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._install_click_handlers()

    def update_date(self, ok_good, ok_bad, ng_good, ng_bad):
        # 预测值
        self.okGoodLab.setText(str(ok_good))
        self.okBadLab.setText(str(ok_bad))
        self.ngGoodLab.setText(str(ng_good))
        self.ngBadLab.setText(str(ng_bad))
        # OK总
        self.okSumLab.setText(str(int(self.okGoodLab.text()) + int(self.okBadLab.text())))
        # NG总
        self.ngSumLab.setText(str(int(self.ngGoodLab.text()) + int(self.ngBadLab.text())))
        # 良好
        self.preOkSumLab.setText(str(int(self.okGoodLab.text()) + int(self.ngGoodLab.text())))
        # 异常
        self.preNgSumLab.setText(str(int(self.okBadLab.text()) + int(self.ngBadLab.text())))

    def _install_click_handlers(self):
        self._label_click_signals = {
            self.okGoodLab: self.okGoodClicked,
            self.okBadLab: self.okBadClicked,
            self.ngGoodLab: self.ngGoodClicked,
            self.ngBadLab: self.ngBadClicked,

            self.okSumLab:self.okSumClicked,
            self.ngSumLab:self.ngSumClicked,
            self.preOkSumLab:self.preOkSumClicked,
            self.preNgSumLab:self.preNgSumClicked,
        }
        for label in self._label_click_signals:
            label.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            signal = self._label_click_signals.get(obj)
            if signal is not None:
                signal.emit()
                return True
        return super().eventFilter(obj, event)
