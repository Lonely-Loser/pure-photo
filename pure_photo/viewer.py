from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6.QtGui import QShortcut, QKeySequence, QCursor
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QStatusBar,
    QWidget,
    QVBoxLayout,
)

from pure_photo.image_container import ImageContainer
from pure_photo.title_bar import TitleBar


class PhotoViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_file = None
        self.is_fullscreen = False
        self.titleBar = None

        self._setup_window()
        self._build_ui()
        self._create_shortcuts()

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    def _setup_window(self):
        """Initialize main window."""
        self.setWindowTitle("Pure Photo")
        self.resize(1200, 800)
        self.setMinimumSize(640, 480)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    def _build_ui(self):
        """
        Create graphics scene and view.
        """
        self.titleBar = TitleBar(self)
        self.imageContainer = ImageContainer()

        self.imageContainer.connect_toolbar(self)

        central = QWidget()

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.titleBar)
        layout.addWidget(self.imageContainer)

        self.setCentralWidget(central)

    def _create_shortcuts(self):
        """
        Create keyboard shortcuts independent from toolbar.
        """
        self.shortcut_zoom_in = QShortcut(QKeySequence("+"), self)
        self.shortcut_zoom_in.activated.connect(self.imageContainer.zoom_in)

        self.shortcut_zoom_out = QShortcut(
            QKeySequence("-"), self
        )
        self.shortcut_zoom_out.activated.connect(self.imageContainer.zoom_out)

        self.shortcut_fit = QShortcut(
            QKeySequence("Space"), self
        )
        self.shortcut_fit.activated.connect(self.imageContainer.fit_image)

    # ------------------------------------------------------------------
    # Image
    # ------------------------------------------------------------------

    def open_image(self):
        """
        Open image file.
        """
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            (
                "Images "
                "(*.png *.jpg *.jpeg *.bmp "
                "*.gif *.tif *.tiff *.webp)"
            )
        )

        if not filename:
            return

        if self.imageContainer.load_image(filename):
            self.current_file = filename
            file_name = Path(filename).name
            self.setWindowTitle(f"{file_name} - Pure Photo")
            self.imageContainer.fit_image()

    # ------------------------------------------------------------------
    # Fullscreen
    # ------------------------------------------------------------------

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.showMaximized()
            self.titleBar.show()
            self.imageContainer.show_toolbar()
            self.imageContainer.show_image_info_bar()
        else:
            self.showFullScreen()
            self.titleBar.hide()
            self.imageContainer.hide_toolbar()
            self.imageContainer.hide_image_info_bar()

        self.is_fullscreen = not self.is_fullscreen

    # ------------------------------------------------------------------
    # Keyboard
    # ------------------------------------------------------------------

    def keyPressEvent(self, event):
        if (
                event.key() == Qt.Key_Escape
                and self.is_fullscreen
        ):
            self.toggle_fullscreen()
            return

        super().keyPressEvent(event)

    # ------------------------------------------------------------------
    # Hover Event
    # ------------------------------------------------------------------

    def _show_tool_bar(self):
        self.imageContainer.show_toolbar()
        # self.imageContainer.show_image_info_bar()

    def _hide_tool_bar(self):
        self.imageContainer.hide_toolbar()
        # self.imageContainer.hide_image_info_bar()

    def _show_info_bar(self):
        self.imageContainer.show_image_info_bar()

    def _hide_info_bar(self):
        self.imageContainer.hide_image_info_bar()

    def eventFilter(self, obj, event):
        if self.is_fullscreen:
            if event.type() == QEvent.Type.MouseMove:
                pos = QCursor.pos()
                top = self.geometry().top()
                bottom = self.geometry().bottom()
                if pos.y() <= top + 5:
                    self._show_tool_bar()
                elif pos.y() >= top + 60:
                    self._hide_tool_bar()

                if pos.y() >= bottom - 5:
                    self._show_info_bar()
                elif pos.y() <= bottom - 35:
                    self._hide_info_bar()

        return super().eventFilter(obj, event)
