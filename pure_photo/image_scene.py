from pathlib import Path

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import (
    QGraphicsPixmapItem,
    QGraphicsScene,
)

from pure_photo.models.image_info import ImageInfo


class ImageScene(QGraphicsScene):
    """
    Graphics scene responsible for managing the image.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap_item = None
        self.current_pixmap = None
        self.image_info = None

    # ------------------------------------------------------------------
    # Image handling
    # ------------------------------------------------------------------

    def load_image(self, filename):
        """
        Load an image into the scene.

        Returns:
            bool: True if loading was successful.
        """
        pixmap = QPixmap(filename)

        if pixmap.isNull():
            return False

        self.clear()
        self.current_pixmap = pixmap
        self.pixmap_item = QGraphicsPixmapItem(self.current_pixmap)

        # کیفیت بهتر هنگام بزرگنمایی
        self.pixmap_item.setTransformationMode(Qt.SmoothTransformation)
        self.addItem(self.pixmap_item)
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
