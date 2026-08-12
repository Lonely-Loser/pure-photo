from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)

from pure_photo.resource_path import resource_path


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("titleBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(36)
        self.setAutoFillBackground(True)

        self._parent = parent

        # ------------------------------------------------------------------
        # Widgets
        # ------------------------------------------------------------------

        self.iconLabel = QLabel()
        self.iconLabel.setObjectName("titleIcon")
        self.iconLabel.setFixedSize(20, 20)

        path = resource_path(
            "resources",
            "icons",
            "full-page-view-100.png"
        )

        self.iconLabel.setPixmap(
            QIcon(path).pixmap(18, 18)
        )

        self.titleLabel = QLabel("Pure Photo")
        self.titleLabel.setObjectName("titleLabel")

        self.minButton = QPushButton("—")
        self.maxButton = QPushButton("□")
        self.closeButton = QPushButton("✕")

        for button in (
            self.minButton,
            self.maxButton,
            self.closeButton,
        ):
            button.setFixedSize(42, 28)
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # ------------------------------------------------------------------
        # Layout
        # ------------------------------------------------------------------

        layout = QHBoxLayout(self)

        layout.setContentsMargins(10, 0, 4, 0)
        layout.setSpacing(6)

        layout.addWidget(self.iconLabel)
        layout.addWidget(self.titleLabel)

        layout.addStretch()

        layout.addWidget(self.minButton)
        layout.addWidget(self.maxButton)
        layout.addWidget(self.closeButton)

        # ------------------------------------------------------------------
        # Signals
        # ------------------------------------------------------------------

        self.closeButton.clicked.connect(parent.close)
        self.minButton.clicked.connect(parent.showMinimized)
        self.maxButton.clicked.connect(self.toggleMaximized)

    # ----------------------------------------------------------------------

    def toggleMaximized(self):
        if self._parent.isMaximized():
            self._parent.showNormal()
            self.maxButton.setText("□")
        else:
            self._parent.showMaximized()
            self.maxButton.setText("❐")