from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QToolButton,
    QSizePolicy,
)


class OverlayToolbar(QWidget):
    openRequested = Signal()
    fullscreenRequested = Signal()
    zoomInRequested = Signal()
    zoomOutRequested = Signal()
    fitRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._create_ui()
        self._connect_signals()

    def _create_ui(self):
        layout = QHBoxLayout(self)

        layout.setContentsMargins(12, 3, 12, 3)
        layout.setSpacing(6)

        self.openButton = self._create_button("resources/icons/opened-folder-100.png")
        self.fullscreenButton = self._create_button("resources/icons/full-page-view-100.png")
        self.zoomInButton = self._create_button("resources/icons/zoom-in-100.png")
        self.zoomOutButton = self._create_button("resources/icons/zoom-out-100.png")
        self.fitButton = self._create_button("resources/icons/zoom-to-fit-100.png")

        spacer = QWidget()
        spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        layout.addWidget(self.openButton)
        layout.addWidget(self.fullscreenButton)

        layout.addWidget(spacer)

        layout.addWidget(self.zoomOutButton)
        layout.addWidget(self.zoomInButton)
        layout.addWidget(self.fitButton)

    def _connect_signals(self):
        self.openButton.clicked.connect(self.openRequested)
        self.fullscreenButton.clicked.connect(
            self.fullscreenRequested
        )
        self.zoomInButton.clicked.connect(
            self.zoomInRequested
        )
        self.zoomOutButton.clicked.connect(
            self.zoomOutRequested
        )
        self.fitButton.clicked.connect(
            self.fitRequested
        )

    def _create_button(self, icon_path: str) -> QToolButton:
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(24, 24))
        button.setFixedSize(34, 34)

        return button
