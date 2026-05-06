from PyQt6.QtWidgets import QLineEdit, QLabel

RBVQ_LENGTH = 6

def mark_invalid(field: QLineEdit, invalid: bool) -> None:
    field.setProperty("invalid", "true" if invalid else "false")
    field.style().unpolish(field)
    field.style().polish(field)

def show_error(label: QLabel, msg: str) -> None:
    label.setText(msg)
    label.show()

def clear_error(label: QLabel, field: QLineEdit) -> None:
    label.hide()
    label.setText("")
    mark_invalid(field, False)

def validate_rbvq(value: str) -> str | None:
    """Return an error message, or None if valid."""
    if not value:
        return "Ce champ est obligatoire."
    if len(value) != RBVQ_LENGTH:
        return f"Doit contenir exactement {RBVQ_LENGTH} caractères."
    return None

def validate_required(value: str) -> str | None:
    """Return an error message, or None if valid."""
    if not value:
        return "Ce champ est obligatoire."
    return None
