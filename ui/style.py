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

QLabel#required_star {
    color: #dd6974;
    font-size: 13px;
    background: transparent;
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

QLineEdit[invalid="true"] {
    border: 1px solid #a13544;
    background-color: #251d1e;
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

QLabel#error_label {
    color: #dd6974;
    font-size: 12px;
    background: transparent;
}
"""
