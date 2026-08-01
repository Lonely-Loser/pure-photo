from PySide6.QtWidgets import QWidget, QVBoxLayout

from pure_photo.image_scene import ImageScene
from image_view import ImageView
from overlay_toolbar import OverlayToolbar
from image_info_bar import ImageInfoBar


class ImageContainer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = ImageScene()
        self.view = ImageView(self.scene)

        self.toolbar = OverlayToolbar(self)
        self.infoBar = ImageInfoBar(self)

        self.toolbar.hide()

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.view)
        layout.addWidget(self.infoBar)

        self.toolbar.resize(
            self.toolbar.sizeHint()
        )

        self.toolbar.raise_()

    def load_image(self, filename):
        success = self.scene.load_image(filename)
        if success:
            self._update_info_bar()
        return success

    def _update_info_bar(self):
        if self.scene.image_info is None:
            return

        self.infoBar.set_image_info(self.scene.image_info)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        margin = 10

        x = (self.width() - self.toolbar.width()) // 2
        y = margin

        self.toolbar.move(x, y)
        self.toolbar.raise_()

    def connect_toolbar(self, viewer):
        self.toolbar.openRequested.connect(viewer.open_image)
        self.toolbar.fullscreenRequested.connect(viewer.toggle_fullscreen)
        self.toolbar.zoomInRequested.connect(self.view.zoom_in)
        self.toolbar.zoomOutRequested.connect(self.view.zoom_out)
        self.toolbar.fitRequested.connect(self.view.fit_image)

    def show_toolbar(self):
        self.toolbar.show()
        self.toolbar.raise_()

    def hide_toolbar(self):
        self.toolbar.hide()

    def zoom_in(self):
        self.view.zoom_in()

    def zoom_out(self):
        self.view.zoom_out()

    def fit_image(self):
        self.view.fit_image()
