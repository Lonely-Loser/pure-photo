from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from models.image_info import ImageInfo


class ImageInfoBar(QWidget):
    """
    Displays current image information.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.file_size = None
        self.setFixedHeight(28)

        self.setObjectName("infoBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._create_widgets()
        self._create_layout()

    # ------------------------------------------------------------------

    def _create_widgets(self):
        self.fileNameLabel = QLabel("No image")
        self.fileNameLabel.setObjectName("infoLabel")

        self.pathLabel = QLabel("")
        self.pathLabel.setObjectName("infoLabel")

        self.formatLabel = QLabel("")
        self.formatLabel.setObjectName("infoLabel")

        self.sizeLabel = QLabel("")
        self.sizeLabel.setObjectName("infoLabel")

        self.resolutionLabel = QLabel("")
        self.resolutionLabel.setObjectName("infoLabel")

        self.zoomLabel = QLabel("100%")
        self.zoomLabel.setObjectName("infoLabel")

    # ------------------------------------------------------------------

    def _create_layout(self):
        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            12, 4, 12, 4
        )
        layout.setSpacing(15)

        layout.addWidget(self.fileNameLabel)
        layout.addWidget(self.pathLabel)
        layout.addWidget(self.formatLabel)
        layout.addWidget(self.sizeLabel)
        layout.addWidget(self.resolutionLabel)

        layout.addStretch()

        layout.addWidget(self.zoomLabel)

    # ------------------------------------------------------------------

    def set_image_info(self, info: ImageInfo):
        self.file_size_formatter(info)
        self.fileNameLabel.setText(f"{info.file_name}    |")
        self.pathLabel.setText(f"{info.directory}    |")
        self.formatLabel.setText(f"{info.image_format}    |")
        self.sizeLabel.setText(f"{self.file_size}    |")
        self.resolutionLabel.setText(f"{info.width} × {info.height}    |")

    def set_zoom(self, zoom_percent: int):
        self.zoomLabel.setText(f"{zoom_percent}%")

    def file_size_formatter(self, info: ImageInfo):
        raw_size = info.file_size / 1024

        if raw_size <= 1024:
            self.file_size = f"{int(raw_size)} Kb"
        else:
            raw_size /= 1024
            raw_size = round(raw_size, 1)
            self.file_size = f"{raw_size} Mb"

