"""Functions responsible for handling files"""

from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
import pandas as pd
from flask import request, send_file, Response
from Row_Eliminator import config


def sanitize_filename(filename: str) -> str:
    """Make filename safe"""
    keep_characters = ('-', '.', '_')
    return "".join(c for c in filename if c.isalnum() or c in keep_characters).rstrip()


def allowed_file(filepath: str) -> bool:
    """Check if file matches filetype criteria"""
    return Path(filepath).suffix.strip('.') in config.ALLOWED_EXTENSIONS


# Upload File Function
def upload_file() -> Path:
    """Retrieve uploaded file from POST and save to uploads directory"""
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        filename = sanitize_filename(file.filename)
        if allowed_file(filename):
            filename = config.UPLOAD_FOLDER / filename
            file.save(filename)
            return filename


def download_file(file: Path) -> Response:
    """Download processed file"""
    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        zf.write(file, file.stem)
    stream.seek(0)
    return send_file(stream, as_attachment=True, download_name='archive.zip')


def load_file(filepath: Path) -> pd.DataFrame:
    """Reads the file into pandas"""
    if filepath.suffix == 'csv':
        return pd.read_csv(filepath)
    elif filepath.suffix == 'xls':
        return pd.read_excel(filepath)
    else:
        return pd.DataFrame()
