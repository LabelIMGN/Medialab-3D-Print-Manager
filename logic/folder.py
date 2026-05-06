import os
import subprocess
import platform
from datetime import date, datetime
from pathlib import Path


def build_folder_name(d: str, t: str, rbvq: str, color: str) -> str:
    return f"{d}-{t}-RBVQ{rbvq}-{color}"


def create_folder(dest: Path, phone: str, notes: str) -> None:
    """Create the project folder and write Notes.txt. Raises on failure."""
    dest.mkdir(parents=True, exist_ok=True)

    lines = [f"Email ou Telephone: {phone}"]
    if notes:
        lines += [
            " ",
            "----------------------------------------------------------------",
            " ",
            notes,
        ]

    (dest / "Notes.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def open_folder(path: Path) -> None:
    """Open a folder in the native file explorer, cross-platform."""
    system = platform.system()
    if system == "Windows":
        os.startfile(str(path))
    elif system == "Darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])
