from datetime import date, datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QFileDialog, QTextEdit, QApplication
)
from PyQt6.QtCore import Qt, QTimer

from ui.style import STYLE
from ui.widgets import (
    make_section, make_divider, make_reset_button,
    make_error_label, make_required_label, make_inline
)
from logic.folder import build_folder_name, create_folder, open_folder
from logic.validation import (
    mark_invalid, show_error, clear_error,
    validate_rbvq, validate_required
)

class FolderCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créateur de dossier")
        self.setMinimumWidth(600)
        self.setStyleSheet(STYLE)
        self._output_dir = Path.cwd()
        self._time_edited = False
        self._date_edited = False
        self._build_ui()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)

    # UI construction --------------------------------

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
        outer.addWidget(make_divider())
        outer.addSpacing(20)

        # Section: Informations
        outer.addWidget(make_section("INFORMATIONS"))
        outer.addSpacing(10)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        # Date
        self.date_input = QLineEdit(date.today().strftime("%Y-%m-%d"))
        self.date_input.setObjectName("mono_input")
        self.date_input.setPlaceholderText("AAAA-MM-JJ")
        self.date_input.setFixedWidth(120)
        self.date_input.textEdited.connect(self._on_date_edited)
        self.reset_date_btn = make_reset_button("↺ Aujourd'hui")
        self.reset_date_btn.clicked.connect(self._reset_date)
        self.reset_date_btn.hide()
        form.addRow("Date :", make_inline(self.date_input, self.reset_date_btn,
                                         note="modifiable si nécessaire"))

        # Time
        self.time_input = QLineEdit(datetime.now().strftime("%Hh%M"))
        self.time_input.setObjectName("mono_input")
        self.time_input.setPlaceholderText("HHhMM")
        self.time_input.setMaxLength(5)
        self.time_input.setFixedWidth(90)
        self.time_input.textEdited.connect(self._on_time_edited)
        self.reset_time_btn = make_reset_button("↺ Maintenant")
        self.reset_time_btn.clicked.connect(self._reset_time)
        self.reset_time_btn.hide()
        form.addRow("Heure :", make_inline(self.time_input, self.reset_time_btn,
                                           note="modifiable si nécessaire"))

        # RBVQ
        self.card_number_input = QLineEdit()
        self.card_number_input.setPlaceholderText("ex: 1234A")
        self.card_number_input.setMaxLength(6)
        self.card_number_input.textChanged.connect(self._on_rbvq_changed)
        self.rbvq_error = make_error_label()
        form.addRow(make_required_label("RBVQ :"), self.card_number_input)
        form.addRow("", self.rbvq_error)

        # Couleur
        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("ex: Rouge")
        self.color_error = make_error_label()
        self.color_input.textChanged.connect(
            lambda t: clear_error(self.color_error, self.color_input) if t.strip() else None
        )
        form.addRow(make_required_label("Couleur :"), self.color_input)
        form.addRow("", self.color_error)

        # Email / Téléphone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("email ou téléphone")
        self.phone_error = make_error_label()
        self.phone_input.textChanged.connect(
            lambda t: clear_error(self.phone_error, self.phone_input) if t.strip() else None
        )
        form.addRow(make_required_label("Email / Téléphone :"), self.phone_input)
        form.addRow("", self.phone_error)

        outer.addLayout(form)
        outer.addSpacing(6)
        legend = QLabel("  *  Champ obligatoire")
        legend.setObjectName("subtitle")
        outer.addWidget(legend)
        outer.addSpacing(16)
        outer.addWidget(make_divider())
        outer.addSpacing(20)

        # Notes
        outer.addWidget(make_section("NOTES"))
        outer.addSpacing(10)
        self.notes_input = QTextEdit()
        self.notes_input.setObjectName("notes_input")
        self.notes_input.setPlaceholderText("Détails supplémentaires sur le projet…")
        self.notes_input.setFixedHeight(90)
        outer.addWidget(self.notes_input)
        outer.addSpacing(20)
        outer.addWidget(make_divider())
        outer.addSpacing(20)

        # Destination
        outer.addWidget(make_section("DOSSIER DE DESTINATION - modifiable si nécessaire"))
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
        outer.addWidget(make_divider())
        outer.addSpacing(20)

        # Create button
        self.create_btn = QPushButton("Créer le dossier")
        self.create_btn.setObjectName("create_btn")
        self.create_btn.setMinimumHeight(42)
        self.create_btn.clicked.connect(self._create_folder)
        outer.addWidget(self.create_btn)

    # Datetime helpers ------------------------------------

    def _datetime_str(self) -> str:
        return datetime.now().strftime("Date : %Y-%m-%d   |   Heure : %H:%M")

    def _set_edited(self, field: QLineEdit, edited: bool):
        field.setProperty("edited", "true" if edited else "false")
        field.style().unpolish(field)
        field.style().polish(field)

    def _tick(self):
        self.subtitle.setText(self._datetime_str())
        if not self._time_edited:
            self.time_input.blockSignals(True)
            self.time_input.setText(datetime.now().strftime("%Hh%M"))
            self.time_input.blockSignals(False)
        if not self._date_edited:
            today = date.today().strftime("%Y-%m-%d")
            if self.date_input.text() != today:
                self.date_input.blockSignals(True)
                self.date_input.setText(today)
                self.date_input.blockSignals(False)

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
        self.time_input.setText(datetime.now().strftime("%Hh%M"))
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
        if text.strip():
            clear_error(self.rbvq_error, self.card_number_input)

    # Directory picker -------------------------------------

    def _pick_directory(self):
        chosen = QFileDialog.getExistingDirectory(
            self, "Changer le dossier de destination (optionnel)", str(self._output_dir)
        )
        if chosen:
            self._output_dir = Path(chosen)
            self.dir_display.setText(chosen)

    # Create action --------------------------------------

    def _create_folder(self):
        rbvq  = self.card_number_input.text().strip()
        color = self.color_input.text().strip()
        phone = self.phone_input.text().strip()
        t     = self.time_input.text().strip()
        d     = self.date_input.text().strip()
        notes = self.notes_input.toPlainText().strip()

        valid = True

        rbvq_err = validate_rbvq(rbvq)
        if rbvq_err:
            mark_invalid(self.card_number_input, True)
            show_error(self.rbvq_error, rbvq_err)
            valid = False
        else:
            clear_error(self.rbvq_error, self.card_number_input)

        color_err = validate_required(color)
        if color_err:
            mark_invalid(self.color_input, True)
            show_error(self.color_error, color_err)
            valid = False
        else:
            clear_error(self.color_error, self.color_input)

        phone_err = validate_required(phone)
        if phone_err:
            mark_invalid(self.phone_input, True)
            show_error(self.phone_error, phone_err)
            valid = False
        else:
            clear_error(self.phone_error, self.phone_input)

        mark_invalid(self.date_input, not d)
        mark_invalid(self.time_input, not t)
        if not d or not t:
            valid = False

        if not valid:
            return

        dest = self._output_dir / build_folder_name(d, t, rbvq, color)

        try:
            create_folder(dest, phone, notes)
            open_folder(dest)
            QApplication.instance().quit()
        except PermissionError:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self, "Erreur de permission",
                f"Impossible de créer le dossier ici :\n{dest}\n\n"
                "Choisissez un autre emplacement."
            )
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Erreur", str(e))
