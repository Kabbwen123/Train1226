from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QMenu, QToolButton, QVBoxLayout, QSizePolicy, QProgressBar


class ModelCardWidget(QFrame):
    clicked = Signal(int)
    editRequested = Signal(int)
    deleteRequested = Signal(int)

    def __init__(self, parent: Optional[QFrame] = None):
        super().__init__(parent)
        self.setObjectName("modelCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setCursor(Qt.PointingHandCursor)
        self._model_id: int | None = None
        self.setStyleSheet(
            """
            #modelCard {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.03);
            }
            #modelCard[selected="true"] {
                border: 1px solid #00A3FF;
                background: rgba(0, 163, 255, 0.06);
            }
            #modelName {
                font-weight: 600;
                font-size: 14px;
            }
            #modelMeta {
                color: #A0A0A0;
                font-size: 12px;
            }
            #trainProgress {
                margin-top: 4px;
            }
            """
        )

        self.nameLabel = QLabel(self)
        self.nameLabel.setObjectName("modelName")
        self.nameLabel.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.nameLabel.setWordWrap(False)
        self.nameLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.nameLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.idLabel = QLabel(self)
        self.idLabel.setObjectName("modelMeta")

        self.menuButton = QToolButton(self)
        self.menuButton.setAutoRaise(True)
        self.menuButton.setCursor(Qt.PointingHandCursor)
        self.menuButton.setIcon(QIcon.fromTheme("more"))
        self.menuButton.setText("···")
        self.menuButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.menuButton.setStyleSheet(
            """
            QToolButton {
                font-weight: 700;
            }
            QToolButton::menu-indicator {
                image: none;
                width: 0px;
                height: 0px;
            }
            """
        )

        menu = QMenu(self.menuButton)
        self._action_edit = menu.addAction("重命名")
        self._action_delete = menu.addAction("删除")
        self.menuButton.setMenu(menu)

        self.timeLabel = QLabel(self)
        self.timeLabel.setObjectName("modelMeta")

        self.progressBar = QProgressBar(self)
        self.progressBar.setObjectName("trainProgress")
        self.progressBar.setRange(0, 100)
        self.progressBar.setTextVisible(True)
        self.progressBar.setVisible(False)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(6)
        top_layout.addWidget(self.nameLabel)
        top_layout.addStretch()
        top_layout.addWidget(self.idLabel)
        top_layout.addWidget(self.menuButton)

        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(12)
        meta_layout.addWidget(self.timeLabel)
        meta_layout.addStretch()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)
        layout.addLayout(top_layout)
        layout.addLayout(meta_layout)
        layout.addWidget(self.progressBar)

        self.setFixedWidth(295)
        self._action_edit.triggered.connect(self._emit_edit)
        self._action_delete.triggered.connect(self._emit_delete)

    def set_model(self, model_id: int, name: str | None, created_at: str | None, ):
        self._model_id = model_id
        display_name = name or "未命名模型"
        self.nameLabel.setText(display_name)
        self.idLabel.setText(f"ID: {model_id}")

        created_text = created_at if created_at else "-"
        self.timeLabel.setText(f"创建时间：{created_text}")

    def model_id(self) -> int | None:
        return self._model_id

    def set_selected(self, selected: bool):
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def set_progress(self, value: float):
        clamped = max(0, min(100, int(round(value))))
        self.progressBar.setValue(clamped)

    def set_progress_visible(self, visible: bool):
        self.progressBar.setVisible(visible)

    # ----------------------- events & signals -----------------------
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton and self._model_id is not None:
            # 避免点击菜单按钮时重复触发
            if not self.menuButton.geometry().contains(event.pos()):
                self.clicked.emit(self._model_id)

    def _emit_edit(self):
        if self._model_id is not None:
            self.editRequested.emit(self._model_id)

    def _emit_delete(self):
        if self._model_id is not None:
            self.deleteRequested.emit(self._model_id)


