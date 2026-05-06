import sys
from datetime import date, datetime
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout,
    QMessageBox, QFrame, QFileDialog, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


STYLE = """
QWidget {
    background-color: #1c1b19;
    color: #cdccca;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 14px;
}

QLabel {
    color: #cdccca;
    background: transparent;
}

QLabel#title {
    font-size: 18px;
    font-weight: 600;
    color: #f0efed;
}

QLabel#subtitle {
    font-size: 12px;
    color: #797876;
}

QLabel#section_label {
    font-size: 11px;
    font-weight: 600;
    color: #797876;
    letter-spacing: 1px;
    text-transform: uppercase;
}

QLineEdit {
    background-color: #22211f;
    border: 1px solid #393836;
    border-radius: 5px;
    padding: 7px 10px;
    color: #cdccca;
    font-size: 14px;
    selection-background-color: #31585c;
}

QLineEdit:focus {
    border: 1px solid #4f98a3;
    background-color: #252422;
}

QLineEdit:hover {
    border: 1px solid #4a4846;
}

QLineEdit#mono_input {
    font-family: 'Consolas', 'Courier New', monospace;
    letter-spacing: 1px;
}

QLineEdit#mono_input[edited="true"] {
    color: #e8af34;
    border-color: #56483e;
}

QTextEdit#notes_input {
    background-color: #22211f;
    border: 1px solid #393836;
    border-radius: 5px;
    padding: 7px 10px;
    color: #cdccca;
    font-size: 14px;
    selection-background-color: #31585c;
}

QTextEdit#notes_input:focus {
    border: 1px solid #4f98a3;
    background-color: #252422;
}

QPushButton#create_btn {
    background-color: #01696f;
    color: #f0efed;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
}

QPushButton#create_btn:hover { background-color: #0c4e54; }
QPushButton#create_btn:pressed { background-color: #0f3638; }
QPushButton#create_btn:disabled { background-color: #2d2c2a; color: #5a5957; }

QPushButton#dir_btn {
    background-color: #2d2c2a;
    color: #cdccca;
    font-size: 13px;
    padding: 7px 12px;
    border: 1px solid #393836;
    border-radius: 5px;
    font-weight: 500;
}

QPushButton#dir_btn:hover { background-color: #393836; border-color: #4a4846; }
QPushButton#dir_btn:pressed { background-color: #22211f; }

QPushButton#reset_btn {
    background-color: transparent;
    color: #797876;
    font-size: 12px;
    padding: 7px 10px;
    border: 1px solid #393836;
    border-radius: 5px;
}

QPushButton#reset_btn:hover {
    color: #cdccca;
    border-color: #4a4846;
    background-color: #2d2c2a;
}

QFrame#divider {
    background-color: #262523;
    border: none;
    max-height: 1px;
}
"""


class FolderCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créateur de dossier")
        self.setMinimumWidth(480)
        self.setStyleSheet(STYLE)
        self._output_dir = Path.cwd()
        self._time_edited = False
        self._date_edited = False
        self._build_ui()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)

    # ── UI construction ──────────────────────────────────────────

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(28, 28, 28, 28)
        outer.setSpacing(0)

        # Header
        title = QLabel("Créer un dossier")
        title.setObjectName("title")
        self.subtitle = QLabel(self._datetime_str())
        self.subtitle.setObjectName("subtitle")
        outer.addWidget(title)
        outer.addSpacing(2)
        outer.addWidget(self.subtitle)
        outer.addSpacing(20)
        outer.addWidget(self._divider())
        outer.addSpacing(20)

        # Section: Informations
        outer.addWidget(self._section("INFORMATIONS"))
        outer.addSpacing(10)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        # Date row
        self.date_input = QLineEdit(date.today().strftime("%Y-%m-%d"))
        self.date_input.setObjectName("mono_input")
        self.date_input.setPlaceholderText("AAAA-MM-JJ")
        self.date_input.setFixedWidth(120)
        self.date_input.textEdited.connect(self._on_date_edited)
        self.date_input.textChanged.connect(self._update_preview)
        self.reset_date_btn = self._reset_button("↺ Aujourd'hui")
        self.reset_date_btn.clicked.connect(self._reset_date)
        self.reset_date_btn.hide()
        form.addRow("Date :", self._inline(self.date_input, self.reset_date_btn, note="modifiable si nécessaire"))

        # Time row
        self.time_input = QLineEdit(datetime.now().strftime("%H%M"))
        self.time_input.setObjectName("mono_input")
        self.time_input.setPlaceholderText("HHMM")
        self.time_input.setMaxLength(5)
        self.time_input.setFixedWidth(90)
        self.time_input.textEdited.connect(self._on_time_edited)
        self.time_input.textChanged.connect(self._update_preview)
        self.reset_time_btn = self._reset_button("↺ Maintenant")
        self.reset_time_btn.clicked.connect(self._reset_time)
        self.reset_time_btn.hide()
        form.addRow("Heure :", self._inline(self.time_input, self.reset_time_btn, note="modifiable si nécessaire"))

        # RBVQ
        self.card_number_input = QLineEdit()
        self.card_number_input.setPlaceholderText("ex: 1234A")
        self.card_number_input.setMaxLength(6)
        self.card_number_input.textChanged.connect(self._on_rbvq_changed)
        form.addRow("RBVQ :", self.card_number_input)

        # Couleur
        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("ex: Rouge")
        self.color_input.textChanged.connect(self._update_preview)
        form.addRow("Couleur :", self.color_input)

        # Email / Téléphone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("email ou téléphone")
        form.addRow("Email / Téléphone :", self.phone_input)

        outer.addLayout(form)
        outer.addSpacing(20)
        outer.addWidget(self._divider())
        outer.addSpacing(20)

        # Section: Notes
        outer.addWidget(self._section("NOTES"))
        outer.addSpacing(10)
        self.notes_input = QTextEdit()
        self.notes_input.setObjectName("notes_input")
        self.notes_input.setPlaceholderText("Détails supplémentaires sur le projet…")
        self.notes_input.setFixedHeight(90)
        outer.addWidget(self.notes_input)
        outer.addSpacing(20)
        outer.addWidget(self._divider())
        outer.addSpacing(20)

        # Section: Destination
        outer.addWidget(self._section("DOSSIER DE DESTINATION - modifiable si nécessaire"))
        outer.addSpacing(10)
        dir_row = QHBoxLayout()
        dir_row.setSpacing(8)
        self.dir_display = QLineEdit(str(self._output_dir))
        self.dir_display.setReadOnly(True)
        self.dir_display.setStyleSheet(
            "QLineEdit { color: #797876; background-color: #201f1d; }"
        )
        dir_btn = QPushButton("Parcourir…")
        dir_btn.setObjectName("dir_btn")
        dir_btn.setFixedWidth(100)
        dir_btn.clicked.connect(self._pick_directory)
        dir_row.addWidget(self.dir_display)
        dir_row.addWidget(dir_btn)
        outer.addLayout(dir_row)
        outer.addSpacing(20)
        outer.addWidget(self._divider())
        outer.addSpacing(20)

        # Preview label (read-only, no editable field)
        outer.addWidget(self._section("APERÇU DU NOM"))
        outer.addSpacing(8)
        self.preview = QLabel(self._folder_name())
        self.preview.setObjectName("preview_value")
        self.preview.setWordWrap(True)
        self.preview.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        outer.addWidget(self.preview)
        outer.addSpacing(20)

        # Create button
        self.create_btn = QPushButton("Créer le dossier")
        self.create_btn.setObjectName("create_btn")
        self.create_btn.setMinimumHeight(42)
        self.create_btn.clicked.connect(self._create_folder)
        outer.addWidget(self.create_btn)

    # ── Widget helpers ───────────────────────────────────────────

    def _section(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("section_label")
        return lbl

    def _divider(self) -> QFrame:
        f = QFrame()
        f.setObjectName("divider")
        f.setFrameShape(QFrame.Shape.HLine)
        f.setFixedHeight(1)
        return f

    def _reset_button(self, label: str) -> QPushButton:
        btn = QPushButton(label)
        btn.setObjectName("reset_btn")
        return btn

    def _inline(self, *widgets, note: str = "") -> QWidget:
        """Pack widgets (and optional note label) into a horizontal container."""
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

    # ── State helpers ────────────────────────────────────────────

    def _datetime_str(self) -> str:
        return datetime.now().strftime("Date : %Y-%m-%d   |   Heure : %H:%M")

    def _folder_name(self) -> str:
        d     = self.date_input.text().strip()      if hasattr(self, "date_input")        else date.today().strftime("%Y-%m-%d")
        t     = self.time_input.text().strip()      if hasattr(self, "time_input")        else datetime.now().strftime("%H%M")
        rbvq  = self.card_number_input.text().strip() if hasattr(self, "card_number_input") else ""
        color = self.color_input.text().strip()     if hasattr(self, "color_input")       else ""
        return f"{d}-{t}-RBVQ{rbvq}-{color}"

    def _update_preview(self):
        self.preview.setText(self._folder_name())

    def _set_edited(self, field: QLineEdit, edited: bool):
        field.setProperty("edited", "true" if edited else "false")
        field.style().unpolish(field)
        field.style().polish(field)

    # ── Tick ─────────────────────────────────────────────────────

    def _tick(self):
        self.subtitle.setText(self._datetime_str())
        if not self._time_edited:
            self.time_input.blockSignals(True)
            self.time_input.setText(datetime.now().strftime("%H%M"))
            self.time_input.blockSignals(False)
            self._update_preview()
        if not self._date_edited:
            today = date.today().strftime("%Y-%m-%d")
            if self.date_input.text() != today:
                self.date_input.blockSignals(True)
                self.date_input.setText(today)
                self.date_input.blockSignals(False)
                self._update_preview()

    # ── Date / time overrides ────────────────────────────────────

    def _on_date_edited(self):
        if not self._date_edited:
            self._date_edited = True
            self._set_edited(self.date_input, True)
            self.reset_date_btn.show()

    def _reset_date(self):
        self._date_edited = False
        self.date_input.setText(date.today().strftime("%Y-%m-%d"))
        self._set_edited(self.date_input, False)
        self.reset_date_btn.hide()

    def _on_time_edited(self):
        if not self._time_edited:
            self._time_edited = True
            self._set_edited(self.time_input, True)
            self.reset_time_btn.show()

    def _reset_time(self):
        self._time_edited = False
        self.time_input.setText(datetime.now().strftime("%H%M"))
        self._set_edited(self.time_input, False)
        self.reset_time_btn.hide()

    def _on_rbvq_changed(self, text: str):
        upper = text.upper()
        if upper != text:
            cursor = self.card_number_input.cursorPosition()
            self.card_number_input.blockSignals(True)
            self.card_number_input.setText(upper)
            self.card_number_input.setCursorPosition(cursor)
            self.card_number_input.blockSignals(False)
        self._update_preview()

    # ── Directory picker ─────────────────────────────────────────

    def _pick_directory(self):
        chosen = QFileDialog.getExistingDirectory(
            self, "Changer le dossier de destination (optionnel)", str(self._output_dir)
        )
        if chosen:
            self._output_dir = Path(chosen)
            self.dir_display.setText(chosen)

    # ── Create action ────────────────────────────────────────────

    def _create_folder(self):
        rbvq  = self.card_number_input.text().strip()
        color = self.color_input.text().strip()
        phone = self.phone_input.text().strip()
        time  = self.time_input.text().strip()
        d     = self.date_input.text().strip()
        notes = self.notes_input.toPlainText().strip()

        missing = [name for name, val in [
            ("RBVQ", rbvq), ("Couleur", color), ("Heure", time), ("Date", d)
        ] if not val]

        if missing:
            QMessageBox.warning(
                self, "Champs manquants",
                f"Veuillez remplir : {', '.join(missing)}"
            )
            return

        dest = self._output_dir / self._folder_name()

        try:
            dest.mkdir(parents=True, exist_ok=True)

            lines = [f"Email ou Telephone: {phone}"]
            if notes:
                lines.append(" ")
                lines.append("----------------------------------------------------------------")
                lines.append(" ")
                lines.append(notes)

            (dest / "Notes.txt").write_text(
                "\n".join(lines) + "\n",
                encoding="utf-8"
            )
            QMessageBox.information(self, "Succès", f'Dossier créé :\n{dest}')
            for inp in (self.card_number_input, self.color_input,
                        self.phone_input):
                inp.clear()
            self.notes_input.clear()
            self._reset_time()
            self._reset_date()
        except PermissionError:
            QMessageBox.critical(
                self, "Erreur de permission",
                f"Impossible de créer le dossier ici :\n{dest}\n\n"
                "Choisissez un autre emplacement."
            )
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = FolderCreator()
    win.show()
    sys.exit(app.exec())
