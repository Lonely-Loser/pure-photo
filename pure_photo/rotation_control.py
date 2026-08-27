from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QToolButton,
)


class RotationControl(QWidget):
    """
    Control for entering and adjusting image rotation angle.
    """

    angleChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._create_ui()
        self._connect_signals()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _create_ui(self):
        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.angleEdit = QLineEdit()
        self.angleEdit.setAlignment(Qt.AlignCenter)
        self.angleEdit.setText("0°")
        self.angleEdit.setFixedSize(58, 34)

        self.increaseButton = self._create_button("▲")
        self.decreaseButton = self._create_button("▼")

        self.increaseButton.setAutoRepeat(True)
        self.increaseButton.setAutoRepeatDelay(300)
        self.increaseButton.setAutoRepeatInterval(150)

        self.decreaseButton.setAutoRepeat(True)
        self.decreaseButton.setAutoRepeatDelay(300)
        self.decreaseButton.setAutoRepeatInterval(150)

        buttonLayout = QVBoxLayout()
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.setSpacing(1)

        buttonLayout.addWidget(self.increaseButton)
        buttonLayout.addWidget(self.decreaseButton)

        layout.addWidget(self.angleEdit)
        layout.addLayout(buttonLayout)

    def _create_button(self, text):
        button = QToolButton()
        button.setText(text)
        button.setFixedSize(24, 16)
        return button

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    def _connect_signals(self):
        self.angleEdit.returnPressed.connect(
            self._apply_text
        )

        self.increaseButton.clicked.connect(
            self._increase_angle
        )

        self.decreaseButton.clicked.connect(
            self._decrease_angle
        )

    # ------------------------------------------------------------------
    # Angle handling
    # ------------------------------------------------------------------

    def _apply_text(self):
        text = self.angleEdit.text().strip()

        if text.endswith("°"):
            text = text[:-1].strip()

        try:
            angle = float(text)
        except ValueError:
            self.set_angle(0.0)
            return

        if not -360.0 <= angle <= 360.0:
            self.set_angle(0.0)
            return

        self.set_angle(angle)
        self.angleChanged.emit(angle)

    def _increase_angle(self):
        angle = self.angle()
        angle = min(angle + 1.0, 360.0)

        self.set_angle(angle)
        self.angleChanged.emit(angle)

    def _decrease_angle(self):
        angle = self.angle()
        angle = max(angle - 1.0, -360.0)

        self.set_angle(angle)
        self.angleChanged.emit(angle)

    def angle(self):
        """
        Return the current angle.
        """
        text = self.angleEdit.text().strip()

        if text.endswith("°"):
            text = text[:-1].strip()

        try:
            return float(text)
        except ValueError:
            return 0.0

    def set_angle(self, angle):
        """
        Set the displayed angle without emitting angleChanged.
        """
        self.angleEdit.setText(f"{float(angle):g}°")
