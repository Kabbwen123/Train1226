from typing import List, Tuple, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QMouseEvent
from PySide6.QtWidgets import QLabel, QFrame, QSizePolicy, QHBoxLayout, QWidget

from Application.ProjectDataClass import AssessResult, ImgDetailData
from Interface.Widget.imgDetailWidget import ImgDetailDialog


class ImageFrame(QFrame):
    def __init__(self, result: Optional[AssessResult], image_path: str):
        super().__init__()
        info = f"标签：{result.tag}\n分数：{result.score}\n检测耗时：{result.detect_time}"
        self.result = ImgDetailData(image_path, result.img_path_cvt, info, result)

class HorizontalContainer(QWidget):
    """
    用于scrollArea
    底部使用的横向容器：从左往右追加控件，
    超出视口宽度时整体左移
    """
    imageClicked = Signal(object)

    def __init__(self, scroll_area):
        super().__init__()
        self.scroll = scroll_area
        self.scroll.setWidgetResizable(True)

        self.padding = 5

        # 内部容器
        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.h_layout = QHBoxLayout(self.container)
        self.h_layout.setContentsMargins(self.padding, self.padding, self.padding, self.padding)
        self.h_layout.setSpacing(self.padding)
        # 让容器大小 = 内容大小
        self.h_layout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)

        self.scroll.setWidget(self.container)

        self.widgets = []

    def frame_size(self) -> int:
        viewport = self.scroll.viewport()
        if not viewport:
            return 0
        viewport_height = viewport.height()
        return max(0, viewport_height - self.padding * 2)

    # -----------------------------------------------------------
    def add_image(self, img_path: str, test_result: Optional[AssessResult]):
        """右侧往左追加图片，按容器高度等比缩放；超限时删除最旧（左侧）"""
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            return

        # 框高度比视口高度少 6px，保持上下各 3px 留白
        frame_height = self.frame_size()

        # 限制图片大小（框在一个正方形里）
        if pixmap.height() > pixmap.width():
            scaled = pixmap.scaledToHeight(int(frame_height), Qt.TransformationMode.SmoothTransformation)
        else:
            scaled = pixmap.scaledToWidth(int(frame_height), Qt.TransformationMode.SmoothTransformation)

        frame = ImageFrame(test_result, img_path)
        frame.setFixedHeight(frame_height)
        frame.setFixedWidth(frame_height)
        frame.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        frame.setObjectName("myFrame")
        frame.setStyleSheet("#myFrame {border: 1px solid white; "
                            "background-color: rgb(0, 0, 0);}")

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(self.padding, self.padding, self.padding, self.padding)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel()
        lbl.setPixmap(scaled)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(lbl)

        # 保留事件对象，便于在回调中标记事件已被处理，避免继续冒泡
        frame.mousePressEvent = lambda event: self._emit_image_clicked(event, frame)
        frame.mouseDoubleClickEvent = lambda event: self._show_image_detail(event, frame)

        self.widgets.append(frame)
        self.h_layout.addWidget(frame)
        self.h_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        self._update_container_position()

    def replace_images(self, imgs: List[Tuple[str, AssessResult]]):
        """批量替换当前所有图片"""
        self.clear_display()
        for path, test_result in imgs:
            self.add_image(path, test_result)

    def clear_display(self):
        while self.widgets:
            old = self.widgets.pop()
            self.h_layout.removeWidget(old)
            old.deleteLater()

    # -----------------------------------------------------------
    def _update_container_position(self):
        """内容宽度 vs 视口宽度 → 决定左移量"""
        self.container.adjustSize()

    def resizeEvent(self, event):
        """ScrollArea 尺寸变化时重新对齐"""
        super().resizeEvent(event)
        # 防止容器还没挂载就调 viewport()
        if self.scroll.viewport():
            self._update_container_position()

    def _emit_image_clicked(self, event: QMouseEvent, frame):
        self.imageClicked.emit(frame.result)
        event.accept()

    def _show_image_detail(self, event: QMouseEvent, frame):
        index = self.widgets.index(frame)
        dlg = ImgDetailDialog([i.result for i in self.widgets], index=index)
        dlg.exec()
        # 明确告诉 Qt 事件已处理，阻止进一步传递给父控件或默认行为
        event.accept()
