from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from pure_photo.models.image_info import ImageInfo


class ImageInfoBar(QWidget):
    """
    Displays current image information.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("infoBar")
        self._create_widgets()
        self._create_layout()
        self._apply_style()

    # ------------------------------------------------------------------

    def _create_widgets(self):
        self.fileNameLabel = QLabel("No image")
        self.pathLabel = QLabel("")
        self.sizeLabel = QLabel("")
        self.formatLabel = QLabel("")
        self.zoomLabel = QLabel("100%")

    # ------------------------------------------------------------------

    def _create_layout(self):
        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            12, 4, 12, 4
        )
        layout.setSpacing(15)

        layout.addWidget(self.fileNameLabel)
        layout.addWidget(self.pathLabel)
        layout.addWidget(self.sizeLabel)
        layout.addWidget(self.formatLabel)

        layout.addStretch()

        layout.addWidget(self.zoomLabel)

    # ------------------------------------------------------------------

    def _apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background: #202020;
                color: #dddddd;
            }

            QLabel {
                color: #dddddd;
            }
        """)

        self.setFixedHeight(28)

    # ------------------------------------------------------------------

    def set_image_info(self, info: ImageInfo):
        self.fileNameLabel.setText(info.file_name)
        self.pathLabel.setText(info.directory)
        self.sizeLabel.setText(f"{info.width} × {info.height}")
        self.formatLabel.setText(info.image_format)

    def set_zoom(self, zoom_percent: int):
        self.zoomLabel.setText(f"{zoom_percent}%")
