import sys
from PySide6.QtWidgets import QApplication
from pure_photo.viewer import PhotoViewer

from pure_photo.resource_path import resource_path


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Pure Photo")
    app.setOrganizationName("QT")

    viewer = PhotoViewer()

    app.installEventFilter(viewer)

    viewer.showMaximized()
    viewer.toggle_fullscreen()

    with open(
            resource_path("resources", "styles", "dark.css"),
            encoding="utf-8",
    ) as f:
        viewer.setStyleSheet(f.read())

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
