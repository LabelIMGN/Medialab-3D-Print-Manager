import sys
import os
from datetime import date
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout,
    QMessageBox, QFrame, QFileDialog
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon


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

QLabel#preview_label {
    color: #797876;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
}

QLabel#preview_value {
    color: #4f98a3;
    font-size: 13px;
    padding: 8px 10px;
    background-color: #22211f;
    border: 1px solid #393836;
    border-radius: 5px;
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

QPushButton#create_btn {
    background-color: #01696f;
    color: #f0efed;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
}

QPushButton#create_btn:hover {
    background-color: #0c4e54;
}

QPushButton#create_btn:pressed {
    background-color: #0f3638;
}

QPushButton#create_btn:disabled {
    background-color: #2d2c2a;
    color: #5a5957;
}

QPushButton#dir_btn {
    background-color: #2d2c2a;
    color: #cdccca;
    font-size: 13px;
    padding: 7px 12px;
    border: 1px solid #393836;
    border-radius: 5px;
    font-weight: 500;
}

QPushButton#dir_btn:hover {
    background-color: #393836;
    border-color: #4a4846;
}

QPushButton#dir_btn:pressed {
    background-color: #22211f;
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
        self.setMinimumWidth(460)
        self.setStyleSheet(STYLE)
        self._output_dir = Path.cwd()
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(28, 28, 28, 28)
        outer.setSpacing(0)

        # ── Header ──────────────────────────────────────────────
        title = QLabel("Créateur de dossier")
        title.setObjectName("title")

        today_str = date.today().strftime("%Y-%m-%d")
        subtitle = QLabel(f"Date : {today_str}")
        subtitle.setObjectName("subtitle")

        outer.addWidget(title)
        outer.addSpacing(2)
        outer.addWidget(subtitle)
        outer.addSpacing(20)
        outer.addWidget(self._divider())
        outer.addSpacing(20)

        # ── Form ────────────────────────────────────────────────
        section = QLabel("INFORMATIONS")
        section.setObjectName("section_label")
        outer.addWidget(section)
        outer.addSpacing(10)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        self.card_number_input   = self._field("ex: 12345A")
        self.letter_input = self._field("ex: A")
        self.color_input  = self._field("ex: Rouge")
        self.phone_input  = self._field("email ou téléphone")

        for inp in (self.card_number_input, self.letter_input,
                    self.color_input, self.phone_input):
            inp.textChanged.connect(self._update_preview)

        form.addRow("RBVQ :",             self.card_number_input)
        form.addRow("Lettre :",           self.letter_input)
        form.addRow("Couleur :",          self.color_input)
        form.addRow("Email / Téléphone :", self.phone_input)
        outer.addLayout(form)

        outer.addSpacing(20)
        outer.addWidget(self._divider())
        outer.addSpacing(20)

        # ── Output directory ────────────────────────────────────
        dir_section = QLabel("DOSSIER DE DESTINATION")
        dir_section.setObjectName("section_label")
        outer.addWidget(dir_section)
        outer.addSpacing(10)

        dir_row = QHBoxLayout()
        dir_row.setSpacing(8)

        self.dir_display = QLineEdit(str(self._output_dir))
        self.dir_display.setReadOnly(True)
        self.dir_display.setObjectName("dir_display")
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

        # ── Preview ─────────────────────────────────────────────
        preview_lbl = QLabel("APERÇU")
        preview_lbl.setObjectName("preview_label")
        outer.addWidget(preview_lbl)
        outer.addSpacing(8)

        self.preview = QLabel(self._folder_name())
        self.preview.setObjectName("preview_value")
        self.preview.setWordWrap(True)
        self.preview.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        outer.addWidget(self.preview)

        outer.addSpacing(20)

        # ── Create button ────────────────────────────────────────
        self.create_btn = QPushButton("Créer le dossier")
        self.create_btn.setObjectName("create_btn")
        self.create_btn.setMinimumHeight(42)
        self.create_btn.clicked.connect(self._create_folder)
        outer.addWidget(self.create_btn)

    # ── Helpers ──────────────────────────────────────────────────

    def _field(self, placeholder: str) -> QLineEdit:
        w = QLineEdit()
        w.setPlaceholderText(placeholder)
        return w

    def _divider(self) -> QFrame:
        f = QFrame()
        f.setObjectName("divider")
        f.setFrameShape(QFrame.Shape.HLine)
        f.setFixedHeight(1)
        return f

    def _folder_name(self) -> str:
        today   = date.today().strftime("%Y-%m-%d")
        letter  = self.letter_input.text().strip() if hasattr(self, "letter_input") else ""
        rbvq    = self.card_number_input.text().strip()   if hasattr(self, "card_number_input")   else ""
        color   = self.color_input.text().strip()  if hasattr(self, "color_input")  else ""
        return f"{today}-{letter}-RBVQ{rbvq}-{color}"

    def _update_preview(self):
        self.preview.setText(self._folder_name())

    def _pick_directory(self):
        chosen = QFileDialog.getExistingDirectory(
            self, "Changer le dossier de destination(optionel)", str(self._output_dir)
        )
        if chosen:
            self._output_dir = Path(chosen)
            self.dir_display.setText(chosen)
            self._update_preview()

    # ── Action ───────────────────────────────────────────────────

    def _create_folder(self):
        rbvq   = self.card_number_input.text().strip()
        letter = self.letter_input.text().strip()
        color  = self.color_input.text().strip()
        phone  = self.phone_input.text().strip()

        missing = [name for name, val in [
            ("RBVQ", rbvq), ("Lettre", letter), ("Couleur", color)
        ] if not val]

        if missing:
            QMessageBox.warning(
                self, "Champs manquants",
                f"Veuillez remplir : {', '.join(missing)}"
            )
            return

        folder_name = self._folder_name()
        dest = self._output_dir / folder_name

        try:
            dest.mkdir(parents=True, exist_ok=True)
            (dest / "Notes.txt").write_text(
                f"Email ou Telephone: {phone}\n",
                encoding="utf-8"
            )
            QMessageBox.information(
                self, "Succès",
                f'Dossier créé :\n{dest}'
            )
            for inp in (self.card_number_input, self.letter_input,
                        self.color_input, self.phone_input):
                inp.clear()
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

