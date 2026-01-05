from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

from PySide6.QtCore import Qt, QPointF, Signal, QTimer
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis


@dataclass
class HistSpec:
    x_min: float = 0.0
    x_max: float = 1.0
    bin_count: int = 100
    bin_width: Optional[float] = None  # 若设置则优先用 bin_width


def _auto_hist_spec(maxv: float) -> HistSpec:
    maxv = max(0.0, float(maxv))
    # maxv 不大且像整数：用 1 分一个 bin（0..maxv）
    if maxv <= 512 and abs(maxv - round(maxv)) < 1e-6:
        return HistSpec(x_min=0.0, x_max=maxv, bin_width=1.0, bin_count=int(maxv) + 1)
    # 否则用 100 bin
    return HistSpec(x_min=0.0, x_max=maxv, bin_count=100, bin_width=None)


def _hist_counts(values: Sequence[float], spec: HistSpec) -> Tuple[List[float], List[int]]:
    if spec.x_max <= spec.x_min:
        return [0.0], [0]

    # bin_width 优先
    if spec.bin_width and spec.bin_width > 0:
        bw = float(spec.bin_width)
        n = max(1, int((spec.x_max - spec.x_min) / bw) + 1)
        counts = [0] * n
        for v in values:
            x = float(v)
            if x < spec.x_min or x > spec.x_max:
                continue
            idx = int((x - spec.x_min) // bw)
            idx = max(0, min(n - 1, idx))
            counts[idx] += 1
        centers = [spec.x_min + (i + 0.5) * bw for i in range(n)]
        return centers, counts

    # bin_count
    n = max(1, int(spec.bin_count))
    bw = (spec.x_max - spec.x_min) / n
    counts = [0] * n
    for v in values:
        x = float(v)
        if x < spec.x_min or x > spec.x_max:
            continue
        idx = int((x - spec.x_min) / bw)
        if idx == n:  # x==x_max
            idx = n - 1
        idx = max(0, min(n - 1, idx))
        counts[idx] += 1
    centers = [spec.x_min + (i + 0.5) * bw for i in range(n)]
    return centers, counts


class _DraggableThresholdLine(QWidget):
    thresholdChanged = Signal(float)

    def __init__(self, chart_view: QChartView, series_for_map: QLineSeries, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self._chart_view = chart_view
        self._chart = chart_view.chart()
        self._series = series_for_map

        self._x_min = 0.0
        self._x_max = 1.0
        self._threshold = 0.0

        self._dragging = False
        self._hit_px = 8

        self._pen = QPen(Qt.black, 2, Qt.SolidLine)
        self._pen.setCosmetic(True)

        self.setParent(chart_view)
        self.raise_()
        self._chart.plotAreaChanged.connect(lambda _: self.update())

    def setRange(self, x_min: float, x_max: float):
        self._x_min = float(x_min)
        self._x_max = float(x_max)
        self.setThreshold(self._threshold)

    def threshold(self) -> float:
        return self._threshold

    def setThreshold(self, x: float):
        x = float(x)
        if x < self._x_min:
            x = self._x_min
        if x > self._x_max:
            x = self._x_max
        self._threshold = x
        self.update()

    def _threshold_x_pixel(self) -> float:
        pos = self._chart.mapToPosition(QPointF(self._threshold, 0.0), self._series)
        return float(pos.x())

    def _hit_test(self, mouse_x: float) -> bool:
        return abs(mouse_x - self._threshold_x_pixel()) <= self._hit_px

    def paintEvent(self, e):
        self.setGeometry(self._chart_view.rect())
        plot = self._chart.plotArea()
        x = self._threshold_x_pixel()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(self._pen)
        painter.drawLine(QPointF(x, plot.top()), QPointF(x, plot.bottom()))
        painter.end()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self._hit_test(e.position().x()):
            self._dragging = True
            self.setCursor(Qt.SizeHorCursor)

    def mouseMoveEvent(self, e):
        if not self._dragging:
            self.setCursor(Qt.SizeHorCursor if self._hit_test(e.position().x()) else Qt.ArrowCursor)
            return
        val = self._chart.mapToValue(QPointF(e.position().x(), e.position().y()), self._series)
        self.setThreshold(val.x())

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._dragging = False
            self.setCursor(Qt.ArrowCursor)
            self.thresholdChanged.emit(self._threshold)


class HistogramThresholdWidget(QWidget):
    """
    两组分数 -> 折线直方图（比例） + 可拖动阈值竖线
    - x_max = max(scores_a + scores_b)
    - y = bin_count / len(list)
    - 支持 attach_lists + 自动刷新（定时检测列表变化）
    """
    thresholdChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._series_a = QLineSeries(name="OK")
        self._series_b = QLineSeries(name="NG")

        self._chart = QChart()
        self._chart.legend().setVisible(True)
        self._chart.addSeries(self._series_a)
        self._chart.addSeries(self._series_b)

        self._axis_x = QValueAxis()
        self._axis_y = QValueAxis()
        self._axis_x.setTitleText("score")
        self._axis_y.setTitleText("ratio")  # 比例
        self._axis_x.setRange(0.0, 1.0)
        self._axis_y.setRange(0.0, 1.0)

        self._chart.addAxis(self._axis_x, Qt.AlignBottom)
        self._chart.addAxis(self._axis_y, Qt.AlignLeft)
        for s in (self._series_a, self._series_b):
            s.attachAxis(self._axis_x)
            s.attachAxis(self._axis_y)

        self._view = QChartView(self._chart)
        self._view.setRenderHint(QPainter.Antialiasing, True)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._view)

        self._line = _DraggableThresholdLine(self._view, self._series_a, parent=self._view)
        self._line.thresholdChanged.connect(self._handle_threshold_changed)
        self._line.thresholdChanged.connect(self.thresholdChanged)

        # 动态绑定列表（引用）
        self._scores_a_ref: Optional[Sequence[float]] = None
        self._scores_b_ref: Optional[Sequence[float]] = None
        self._last_signature: Optional[Tuple[int, int, float]] = None  # (lenA, lenB, maxv)
        self._threshold_initialized = False
        self._threshold_locked = False
        self._suppress_threshold_lock = False

        self._poll_timer = QTimer(self)
        self._poll_timer.setInterval(200)  # 默认 200ms 检测一次
        self._poll_timer.timeout.connect(self._poll_refresh)

    # ----------- 推荐：绑定列表，让它自动刷新 -----------
    def attach_lists(self, scores_a: Sequence[float], scores_b: Sequence[float], *, poll_ms: int = 200):
        """保存外部列表引用；如果外部 append，这里能自动检测并刷新。"""
        self._scores_a_ref = scores_a
        self._scores_b_ref = scores_b
        self._poll_timer.setInterval(max(30, int(poll_ms)))
        self.refresh(force=True)
        self._poll_timer.start()

    def detach_lists(self):
        self._poll_timer.stop()
        self._scores_a_ref = None
        self._scores_b_ref = None
        self._last_signature = None

    # ----------- 推荐：你在 append 后手动调用 refresh()（更快） -----------
    def refresh(self, *, force: bool = False):
        """根据当前绑定列表刷新图。force=True 强制重算。"""
        a = list(self._scores_a_ref or [])
        b = list(self._scores_b_ref or [])
        self.set_data(a, b, force=force)

    # ----------- 核心：设置数据（你也可直接用它） -----------
    def set_data(self, scores_a: Sequence[float], scores_b: Sequence[float], *, force: bool = False):
        maxv = 0.0
        if scores_a:
            maxv = max(maxv, float(max(scores_a)))
        if scores_b:
            maxv = max(maxv, float(max(scores_b)))
        maxv = max(0.0, maxv)

        signature = (len(scores_a), len(scores_b), maxv)
        if (not force) and self._last_signature == signature:
            return
        self._last_signature = signature

        spec = _auto_hist_spec(maxv)

        xs_a, cnt_a = _hist_counts(scores_a, spec)
        xs_b, cnt_b = _hist_counts(scores_b, spec)

        total_a = max(1, len(scores_a))
        total_b = max(1, len(scores_b))
        ya = [c / total_a for c in cnt_a]  # 比例
        yb = [c / total_b for c in cnt_b]

        self._series_a.clear()
        self._series_b.clear()
        for x, y in zip(xs_a, ya):
            self._series_a.append(float(x), float(y))
        for x, y in zip(xs_b, yb):
            self._series_b.append(float(x), float(y))

        x_max = maxv if maxv > 0 else 1.0
        self._axis_x.setRange(0.0, x_max)

        self._axis_y.setRange(0.0, 1.0)

        # 更新阈值线范围，并夹住当前阈值
        self._line.setRange(0.0, self._axis_x.max())
        self._line.setThreshold(self._line.threshold())

        if (scores_a or scores_b) and (not self._threshold_locked):
            threshold = self._default_threshold(xs_a, ya, xs_b, yb, self._axis_x.min(), self._axis_x.max())
            self._set_threshold_safely(threshold)
            self.thresholdChanged.emit(threshold)
            self._threshold_initialized = True

    @staticmethod
    def _default_threshold(
            xs_a: Sequence[float],
            ys_a: Sequence[float],
            xs_b: Sequence[float],
            ys_b: Sequence[float],
            x_min: float,
            x_max: float,
    ) -> float:
        def _mean(xs: Sequence[float], ys: Sequence[float]) -> Optional[float]:
            if not xs or not ys:
                return None
            total = 0.0
            weight = 0.0
            for x, y in zip(xs, ys):
                total += float(x) * float(y)
                weight += float(y)
            if weight <= 0.0:
                return None
            return total / weight

        mean_a = _mean(xs_a, ys_a)
        mean_b = _mean(xs_b, ys_b)
        if mean_a is not None and mean_b is not None:
            mid_point = (mean_a + mean_b) / 2.0
        else:
            mid_point = x_min + (x_max - x_min) / 2.0

        intersections = []
        count = min(len(xs_a), len(xs_b), len(ys_a), len(ys_b))
        if count >= 2:
            for i in range(count - 1):
                x1 = float(xs_a[i])
                x2 = float(xs_a[i + 1])
                d1 = float(ys_a[i]) - float(ys_b[i])
                d2 = float(ys_a[i + 1]) - float(ys_b[i + 1])
                if d1 == 0.0:
                    intersections.append(x1)
                    continue
                if d2 == 0.0:
                    intersections.append(x2)
                    continue
                if d1 * d2 < 0.0:
                    ratio = d1 / (d1 - d2)
                    intersections.append(x1 + (x2 - x1) * ratio)
        if intersections:
            return float(min(intersections, key=lambda x: abs(x - mid_point)))
        return float(mid_point)

    def set_threshold(self, x: float):
        self._threshold_locked = True
        self._set_threshold_safely(x)

    def threshold(self) -> float:
        return self._line.threshold()

    def _handle_threshold_changed(self, _value: float):
        if not self._suppress_threshold_lock:
            self._threshold_locked = True

    def _set_threshold_safely(self, value: float):
        self._suppress_threshold_lock = True
        self._line.setThreshold(value)
        self._suppress_threshold_lock = False

    # ----------- 内部：定时检测列表是否变化 -----------
    def _poll_refresh(self):
        a = self._scores_a_ref or []
        b = self._scores_b_ref or []

        try:
            len_a = len(a)
            len_b = len(b)
            maxv = 0.0
            if len_a:
                maxv = max(maxv, float(max(a)))
            if len_b:
                maxv = max(maxv, float(max(b)))
            maxv = max(0.0, maxv)
        except Exception:
            # 外部列表可能在别的线程修改导致瞬时异常，下一次再试
            return

        sig = (len_a, len_b, maxv)
        if sig != self._last_signature:
            self.set_data(list(a), list(b), force=True)
