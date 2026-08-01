from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QCursor
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsView,
)


class ImageView(QGraphicsView):
    """
    Graphics view used to display and manipulate images.
    """
    zoomChanged = Signal(int)
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)

        # Zoom settings
        self.zoom_factor = 1.15
        self.min_zoom = 0.1
        self.max_zoom = 10.0

        # Cursor settings
        self.cursor_hide_delay = 1000
        self.cursor_hidden = False
        self.cursor_timer = QTimer(self)
        self.cursor_timer.setSingleShot(True)
        self.cursor_timer.timeout.connect(self.hide_cursor)

        self._setup_view()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def _setup_view(self):
        """Configure graphics view."""
        self.setBackgroundBrush(QColor(0, 0, 0))
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Zoom around mouse position
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        # Enable drag/pan
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setInteractive(True)
        self.setMouseTracking(True)
        self.show_cursor()

    # ------------------------------------------------------------------
    # Image display
    # ------------------------------------------------------------------
    def fit_image(self):
        """
        Fit image inside the window.
        """
        if not self.scene().has_image():
            return

        self.reset_zoom()

        self.fitInView(
            self.scene().pixmap_item,
            Qt.KeepAspectRatio
        )

        self._emit_zoom_changed()

    def center_image(self):
        """
        Center image in the view.
        """
        if not self.scene().has_image():
            return

        self.centerOn(
            self.scene().pixmap_item
        )

    def zoom_in(self):
        current_zoom = self.transform().m11()
        if current_zoom >= self.max_zoom:
            return

        self.scale(self.zoom_factor, self.zoom_factor)
        self._emit_zoom_changed()

    def zoom_out(self):
        current_zoom = self.transform().m11()
        if current_zoom <= self.min_zoom:
            return

        factor = 1 / self.zoom_factor
        self.scale(factor, factor)
        self._emit_zoom_changed()

    def reset_zoom(self):
        self.resetTransform()
        self._emit_zoom_changed()

    def _emit_zoom_changed(self):
        zoom = self.transform().m11()
        zoom_percent = round(zoom * 100)

        self.zoomChanged.emit(zoom_percent)

    # ------------------------------------------------------------------
    # Wheel zoom
    # ------------------------------------------------------------------
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    # ------------------------------------------------------------------
    # Cursor handling
    # ------------------------------------------------------------------

    def reset_cursor_timer(self):
        """
        Restart cursor hide timer.
        """
        self.show_cursor()
        self.cursor_timer.start(self.cursor_hide_delay)

    def hide_cursor(self):
        """
        Hide mouse cursor.
        """
        self.viewport().setCursor(Qt.BlankCursor)
        self.cursor_hidden = True

    def show_cursor(self):
        """
        Show mouse cursor.
        """
        self.viewport().setCursor(Qt.ArrowCursor)
        self.cursor_hidden = False

    def mouseMoveEvent(self, event):
        """
        Handle mouse movement.
        """
        self.reset_cursor_timer()
        super().mouseMoveEvent(event)
