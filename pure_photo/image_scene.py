from pathlib import Path

from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QPixmap, QImageReader
from PySide6.QtWidgets import (
    QGraphicsPixmapItem,
    QGraphicsScene,
)

from pure_photo.models.image_info import ImageInfo


class ImageScene(QGraphicsScene):
    """
    Graphics scene responsible for managing the image.
    """

    SUPPORTED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".gif",
        ".tif",
        ".tiff",
        ".webp",
    }

    rotationChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap_item = None
        self.current_pixmap = None
        self.image_info = None
        self.rotation = 0.0

    # ------------------------------------------------------------------
    # Image handling
    # ------------------------------------------------------------------

    def load_image(self, filename):
        """
        Load an image into the scene.

        Returns:
            bool: True if loading was successful.
        """

        reader = QImageReader(filename)
        reader.setAutoTransform(True)

        image = reader.read()

        if image.isNull():
            return False

        pixmap = QPixmap.fromImage(image)

        self.clear()
        self.current_pixmap = pixmap
        self.pixmap_item = QGraphicsPixmapItem(self.current_pixmap)

        # Rotate around the center of the image
        self.pixmap_item.setTransformOriginPoint(
            self.pixmap_item.boundingRect().center()
        )

        # کیفیت بهتر هنگام بزرگنمایی
        self.pixmap_item.setTransformationMode(Qt.SmoothTransformation)

        self.rotation = 0.0
        self.addItem(self.pixmap_item)
        self.rotationChanged.emit(self.rotation)

        self._update_scene_rect()

        path = Path(filename)

        self.image_info = ImageInfo(
            file_path=path,
            width=pixmap.width(),
            height=pixmap.height(),
            image_format=path.suffix.lstrip(".").upper(),
            file_size=path.stat().st_size,
        )

        return True

    def clear_image(self):
        """
        Remove current image.
        """
        self.clear()
        self.pixmap_item = None
        self.current_pixmap = None
        self.image_info = None
        self.rotation = 0.0

    @classmethod
    def is_supported_image(cls, filename):
        """
        Check whether the file is a supported image.
        """
        return Path(filename).suffix.lower() in cls.SUPPORTED_EXTENSIONS

    # ------------------------------------------------------------------
    # Rotation
    # ------------------------------------------------------------------

    def rotate_left(self):
        """
        Rotate the image 90 degrees counter-clockwise.
        """
        if not self.pixmap_item:
            return

        self.set_rotation(self.rotation - 90)

    def rotate_right(self):
        """
        Rotate the image 90 degrees clockwise.
        """
        if not self.pixmap_item:
            return

        self.set_rotation(self.rotation + 90)

    def set_rotation(self, angle):
        """
        Set an absolute rotation angle.
        """
        if not self.pixmap_item:
            return

        self.rotation = float(angle)
        self.pixmap_item.setRotation(self.rotation)
        self.rotationChanged.emit(self.rotation)

    def reset_rotation(self):
        """
        Reset the image rotation to the default orientation.
        """
        self.set_rotation(0.0)

    # ------------------------------------------------------------------
    # Scene information
    # ------------------------------------------------------------------
    def has_image(self):
        """
        Check if an image exists.
        """
        return self.pixmap_item is not None

    def image_size(self):
        """
        Return image size.
        """
        if not self.current_pixmap:
            return None

        return self.current_pixmap.size()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _update_scene_rect(self):
        """
        Create a larger scene area around the image
        to allow free movement.
        """
        if not self.pixmap_item:
            return

        image_rect = self.pixmap_item.boundingRect()
        margin = 10000

        scene_rect = image_rect.adjusted(
            -margin,
            -margin,
            margin,
            margin
        )

        self.setSceneRect(scene_rect)
