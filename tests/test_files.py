"""Unit tests for files.py"""

from pathlib import Path
import pandas as pd
from Row_Eliminator import files


# sanitize_filename() tests
def test_sanitize_filename():
    ...


# allowed_file() tests
def test_allowed_file_csv():
    assert files.allowed_file("filename.csv")


def test_allowed_file_xls():
    assert files.allowed_file("filename.xls")


def test_allowed_file_jpg():
    assert not files.allowed_file("filename.jpg")


def test_allowed_file_csv_jpg():
    assert not files.allowed_file("filename.csv.jpg")


# upload_file() tests
def test_upload_file():
    ...


# download_file() tests
def test_download_file():
    ...


# load_file_to_db() tests
def test_load_file_csv():
    output = files.load_file(Path('tests/test_db.csv'))
    assert isinstance(output, pd.DataFrame), "Did not return pandas DataFrame"


def test_load_file_xls():
    output = files.load_file(Path('tests/test_db.xls'))
    assert isinstance(output, pd.DataFrame), "Did not return pandas DataFrame"
