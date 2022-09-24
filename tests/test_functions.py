"""Unit tests for functions.py"""

from Row_Eliminator import functions

def test_allowed_file_csv():
    assert functions.allowed_file("filename.csv")

def test_allowed_file_xls():
    assert functions.allowed_file("filename.xls")

def test_allowed_file_jpg():
    assert not functions.allowed_file("filename.jpg")

def test_allowed_file_csv_jpg():
    assert not functions.allowed_file("filename.csv.jpg")