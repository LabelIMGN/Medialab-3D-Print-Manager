from PyQt6.QtWidgets import QWidget, QLabel
import re

RBVQ_LENGTH = 6

def mark_invalid(field: QWidget, invalid: bool) -> None:
    field.setProperty("invalid", "true" if invalid else "false")
    field.style().unpolish(field)
    field.style().polish(field)

def show_error(label: QLabel, msg: str) -> None:
    label.setText(msg)
    label.show()

def clear_error(label: QLabel, field: QWidget) -> None:
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

def validate_date(value: str) -> str | None:
    """Return an error message, or None if valid (expects YYYY-MM-DD)."""
    if not value:
        return "Ce champ est obligatoire."
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return "Format invalide. Utilisez AAAA-MM-JJ."
    from datetime import date
    try:
        date.fromisoformat(value)
    except ValueError:
        return "Date invalide (ex: mois ou jour hors limite)."
    return None

def validate_time(value: str) -> str | None:
    """Return an error message, or None if valid (expects HHhMM)."""
    if not value:
        return "Ce champ est obligatoire."
    if not re.fullmatch(r"\d{2}h\d{2}", value):
        return "Format invalide. Utilisez HHhMM (ex: 14h30)."
    hh, mm = int(value[:2]), int(value[3:])
    if not (0 <= hh <= 23 and 0 <= mm <= 59):
        return "Heure invalide (00h00 à 23h59)."
    return None

def validate_required(value: str) -> str | None:
    """Return an error message, or None if valid."""
    if not value:
        return "Ce champ est obligatoire."
    return None

def format_phone(raw: str) -> str | None:
    """Strip non-digits and reformat to ###-###-####. Returns None if not 10 digits."""
    digits = re.sub(r'\D', '', raw)
    if len(digits) == 11 and digits[0] == '1':
        digits = digits[1:]  # strip leading country code
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    return None

def validate_contact(value: str) -> str | None:
    """Return an error message, or None if valid (email or ###-###-#### phone)."""
    if not value:
        return "Ce champ est obligatoire."
    if '@' in value:
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
            return "Adresse courriel invalide."
        return None
    formatted = format_phone(value)
    if formatted is None:
        return "Format invalide. Entrez un courriel ou un numéro à 10 chiffres."
    return None
