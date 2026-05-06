from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt

def make_section(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("section_label")
    return lbl

def make_divider() -> QFrame:
    f = QFrame()
    f.setObjectName("divider")
    f.setFrameShape(QFrame.Shape.HLine)
    f.setFixedHeight(1)
    return f

def make_reset_button(label: str) -> QPushButton:
    btn = QPushButton(label)
    btn.setObjectName("reset_btn")
    return btn

def make_error_label() -> QLabel:
    lbl = QLabel("")
    lbl.setObjectName("error_label")
    lbl.hide()
    return lbl

def make_required_label(text: str) -> QWidget:
    """Form row label with a red star indicating a required field."""
    container = QWidget()
    container.setStyleSheet("background: transparent;")
    row = QHBoxLayout(container)
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(2)
    lbl = QLabel(text)
    # star = QLabel("✦")
    star = QLabel("*")
    star.setObjectName("required_star")
    row.addWidget(lbl)
    row.addWidget(star)
    row.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    return container

def make_inline(*widgets: QWidget, note: str = "") -> QWidget:
    """Pack widgets (and an optional note label) into a horizontal row."""
    container = QWidget()
    container.setStyleSheet("background: transparent;")
    row = QHBoxLayout(container)
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(8)
    for w in widgets:
        row.addWidget(w)
    if note:
        lbl = QLabel(note)
        lbl.setObjectName("subtitle")
        row.addWidget(lbl)
    row.addStretch()
    return container
