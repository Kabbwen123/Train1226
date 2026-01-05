from math import ceil
from typing import List, Optional, Tuple

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from Application.ProjectDataClass import AssessResult
from Interface.UI.assess.imgUI import Ui_Form
from Interface.Widget.assess.horizontalContainerWidget import HorizontalContainer


class ImgWidget(QWidget, Ui_Form):
    _DEFAULT_PAGE_SIZE = 10
    imageClicked = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._images: List[Tuple[str, Optional[AssessResult]]] = []
        self._current_page = 0
        self._show_converted = False

        self.scroll_container = HorizontalContainer(self.scrollArea)
        self._page_size = self._DEFAULT_PAGE_SIZE

        self.firstPageBtn.clicked.connect(self._go_first_page)
        self.prevBtn.clicked.connect(self._go_prev_page)
        self.nextBtn.clicked.connect(self._go_next_page)
        self.lastPageBtn.clicked.connect(self._go_last_page)
        self.scroll_container.imageClicked.connect(self.imageClicked.emit)

        self._update_page_size()
        self._refresh_page()

    def set_show_converted(self, show_converted: bool):
        if self._show_converted == show_converted:
            return
        self._show_converted = show_converted
        self._images = [
            (self._resolve_image_path(result, img_path), result)
            for img_path, result in self._images
        ]
        self._refresh_page()

    def set_images(self, images: List[Tuple[str, Optional[AssessResult]]]):
        resolved_images = []
        for img_path, result in images:
            resolved_path = self._resolve_image_path(result, img_path)
            if resolved_path:
                resolved_images.append((resolved_path, result))
        self._images = resolved_images
        self._current_page = 1 if self._images else 0
        self._refresh_page()

    def add_image(self, img_path: str, test_result: Optional[AssessResult]):
        previous_pages = self._page_count()
        resolved_path = self._resolve_image_path(test_result, img_path)
        if resolved_path:
            self._images.append((resolved_path, test_result))
        if self._current_page == previous_pages:
            self._current_page = self._page_count()
        elif self._current_page == 0:
            self._current_page = 1
        self._refresh_page()

    def clear_images(self):
        self._images.clear()
        self._current_page = 0
        self._refresh_page()

    def _page_count(self) -> int:
        if not self._images:
            return 0
        return ceil(len(self._images) / self._page_size)

    def _calculate_page_size(self) -> int:
        viewport = self.scrollArea.viewport()
        if not viewport:
            return self._DEFAULT_PAGE_SIZE

        frame_size = self.scroll_container.frame_size()
        if frame_size <= 0:
            return self._DEFAULT_PAGE_SIZE

        padding = self.scroll_container.padding
        available_width = viewport.width()
        per_item = frame_size + padding
        if per_item <= 0:
            return self._DEFAULT_PAGE_SIZE

        return max(1, (available_width - padding) // per_item)

    def _resolve_image_path(self, result: Optional[AssessResult], fallback_path: Optional[str]) -> Optional[str]:
        if result:
            if self._show_converted and result.img_path_cvt:
                return result.img_path_cvt
            return result.img_path
        return fallback_path

    def _update_page_size(self):
        page_size = self._calculate_page_size()
        if page_size != self._page_size:
            self._page_size = page_size

    def _refresh_page(self):
        self._update_page_size()
        total_pages = self._page_count()
        if total_pages == 0:
            self._current_page = 0
            self.scroll_container.clear_display()
            self.pageLab.setText("0/0")
            self._set_nav_enabled(False)
            return

        self._current_page = max(1, min(self._current_page, total_pages))
        start = (self._current_page - 1) * self._page_size
        end = start + self._page_size
        self.scroll_container.replace_images(self._images[start:end])

        self.pageLab.setText(f"{self._current_page}/{total_pages}")
        self.firstPageBtn.setEnabled(self._current_page > 1)
        self.prevBtn.setEnabled(self._current_page > 1)
        self.nextBtn.setEnabled(self._current_page < total_pages)
        self.lastPageBtn.setEnabled(self._current_page < total_pages)

    def _set_nav_enabled(self, enabled: bool):
        self.firstPageBtn.setEnabled(enabled)
        self.prevBtn.setEnabled(enabled)
        self.nextBtn.setEnabled(enabled)
        self.lastPageBtn.setEnabled(enabled)

    def _go_first_page(self):
        if self._current_page > 1:
            self._current_page = 1
            self._refresh_page()

    def _go_prev_page(self):
        if self._current_page > 1:
            self._current_page -= 1
            self._refresh_page()

    def _go_next_page(self):
        total_pages = self._page_count()
        if self._current_page < total_pages:
            self._current_page += 1
            self._refresh_page()

    def _go_last_page(self):
        total_pages = self._page_count()
        if total_pages and self._current_page != total_pages:
            self._current_page = total_pages
            self._refresh_page()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._refresh_page()
        self._refresh_page()