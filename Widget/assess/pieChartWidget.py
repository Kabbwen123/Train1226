from __future__ import annotations

from typing import Dict

from PySide6.QtCore import Qt, Signal, QMargins
from PySide6.QtGui import QPainter, QColor, QCursor
from PySide6.QtCharts import QChartView, QChart, QPieSeries, QPieSlice
from PySide6.QtWidgets import QGraphicsSimpleTextItem, QToolTip


class PieChartWidget(QChartView):
    """
    可复用饼图控件
    ---------------------------------
    使用示例（纯代码方式）：
        pie = PieChartWidget()
        pie.set_title("检测统计")
        pie.set_color_map({
            "OK": "#4CAF50",       # 绿色
            "NG": "#F44336",       # 红色
            "未判定": "#9E9E9E",   # 灰色
        })
        pie.set_data({
            "OK": 12,
            "NG": 3,
            "未判定": 5,
        })
    在 Qt Designer 中：
        1. 拖一个 QWidget 占位
        2. 右键 -> Promote to...
           - Promoted class name: PieChartWidget
           - Header file: piechartwidget
        3. 在代码中 from widgets.piechartwidget import PieChartWidget
           然后照常 setupUi(self)
    """

    # 点击某个扇形时发出：label, value
    sliceClicked = Signal(str, float)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 图表本体
        self._chart = QChart()
        self._chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self._chart.legend().setVisible(False)

        self.setChart(self._chart)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setMouseTracking(True)

        # 饼图序列
        self._series = QPieSeries()
        self._series.setPieSize(0.9)
        self._chart.addSeries(self._series)

        # 是否在标签中显示百分比
        self._show_percent = True
        # 标签 -> 颜色 映射
        self._color_map: dict[str, QColor] = {}
        self._hovered_slice: QPieSlice | None = None
        self._total_value: float = 0.0
        # 标题文本项
        self._title_item = QGraphicsSimpleTextItem("", self._chart)
        self._title_item.setVisible(False)

        self._apply_compact_margins()

    # ---------- 对外接口 ----------

    def set_title(self, title: str):
        """设置饼图标题"""
        self._title_item.setText(title)
        self._title_item.setVisible(bool(title))
        self._update_title_position()

    def set_show_percent(self, enabled: bool):
        """是否在标签文字中显示百分比"""
        self._show_percent = enabled
        # 重新渲染一下标签
        self._update_labels()

    def clear(self):
        """清空饼图数据"""
        self._series.clear()

    def set_color_map(self, color_map: dict[str, "QColor | str"]):
        """
        设置每个标签对应的颜色：
        例如：{"OK": "green", "NG": "#FF0000"}
        """
        self._color_map.clear()
        for k, v in color_map.items():
            if isinstance(v, QColor):
                self._color_map[k] = v
            else:
                self._color_map[k] = QColor(v)

    def set_data(self, data: Dict[str, float]):
        existing = self._existing_slices_by_label()

        if not data:
            for pie_slice in list(existing.values()):
                self._series.remove(pie_slice)
            if self._hovered_slice:
                self._hovered_slice = None
            self._total_value = 0.0
            return

        total = sum(value for value in data.values() if value >= 0)
        self._total_value = total if total > 0 else 1.0

        for label, pie_slice in list(existing.items()):
            if label not in data:
                if self._hovered_slice is pie_slice:
                    self._hovered_slice = None
                self._series.remove(pie_slice)

        for label, value in data.items():
            if value < 0:
                continue

            pie_slice = existing.get(label)
            if pie_slice is None:
                pie_slice = self._series.append(label, value)
                pie_slice.setProperty("base_label", label)
            else:
                pie_slice.setValue(value)

            pie_slice.setProperty("base_label", label)
            self._bind_slice_signals(pie_slice, label)
            if label in self._color_map:
                pie_slice.setColor(self._color_map[label])

            self._apply_slice_label(pie_slice, label, self._total_value)
            pie_slice.setLabelVisible(False)

        self._update_title_position()

    # ---------- 内部辅助 ----------

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_title_position()

    def _update_labels(self):
        """当 show_percent 改变时，更新现有 slice 的标签"""
        slices = self._series.slices()
        if not slices:
            return

        total = sum(s.value() for s in slices) or 1.0

        for sl in slices:
            label = self._base_label_from_slice(sl)
            self._apply_slice_label(sl, label, total)
            sl.setLabelVisible(False)

    def _on_slice_hover(self, pie_slice: QPieSlice, label: str, state: bool):
        value = pie_slice.value()
        total = self._total_value or 1.0
        if state:
            if self._hovered_slice and self._hovered_slice is not pie_slice:
                self._hovered_slice.setExploded(False)
            pie_slice.setExploded(True)
            self._hovered_slice = pie_slice

            percent = value / total * 100.0 if total else 0.0
            info = f"{label}: {value} ({percent:.1f}%)"
            QToolTip.showText(QCursor.pos(), info, self)
        else:
            pie_slice.setExploded(False)
            if self._hovered_slice is pie_slice:
                self._hovered_slice = None

    def leaveEvent(self, event):
        # 鼠标离开饼图区域时，收起悬浮效果与提示
        if self._hovered_slice:
            self._hovered_slice.setExploded(False)
            self._hovered_slice = None
        QToolTip.hideText()
        super().leaveEvent(event)

    def _update_title_position(self):
        if not self._title_item.text():
            self._title_item.setVisible(False)
            self._apply_compact_margins()
            return

        plot_area = self._chart.plotArea()
        text_rect = self._title_item.boundingRect()
        gap = 6

        x = plot_area.center().x() - text_rect.width() / 2
        y = plot_area.bottom() + gap

        self._title_item.setPos(x, y)
        self._title_item.setVisible(True)

        bottom_padding = int(text_rect.height() + gap * 2)
        self._apply_compact_margins(bottom_padding=bottom_padding)

    def _apply_compact_margins(self, bottom_padding: int | float = 0):
        margin = 4
        self._chart.setMargins(QMargins(margin, margin, margin, margin + int(bottom_padding)))
        self.setContentsMargins(0, 0, 0, 0)

    def _handle_slice_clicked(self, label: str, pie_slice: QPieSlice):
        self.sliceClicked.emit(label, pie_slice.value())

    def _handle_slice_hovered(self, pie_slice: QPieSlice, label: str, state: bool):
        self._on_slice_hover(pie_slice, label, state)

    def _bind_slice_signals(self, pie_slice: QPieSlice, label: str):
        try:
            pie_slice.clicked.disconnect()
        except TypeError:
            pass
        try:
            pie_slice.hovered.disconnect()
        except TypeError:
            pass
        pie_slice.clicked.connect(lambda lbl=label, sl=pie_slice: self._handle_slice_clicked(lbl, sl))
        pie_slice.hovered.connect(lambda state, lbl=label, sl=pie_slice: self._handle_slice_hovered(sl, lbl, state))

    def _apply_slice_label(self, pie_slice: QPieSlice, label: str, total: float):
        if self._show_percent:
            percent = pie_slice.value() / total * 100.0 if total else 0.0
            pie_slice.setLabel(f"{label} {percent:.1f}%")
        else:
            pie_slice.setLabel(label)

    def _base_label_from_slice(self, pie_slice: QPieSlice) -> str:
        stored = pie_slice.property("base_label")
        if isinstance(stored, str) and stored:
            return stored
        label = pie_slice.label().split()[0]
        pie_slice.setProperty("base_label", label)
        return label

    def _existing_slices_by_label(self) -> Dict[str, QPieSlice]:
        slices = {}
        for pie_slice in self._series.slices():
            label = self._base_label_from_slice(pie_slice)
            slices[label] = pie_slice
        return slices

