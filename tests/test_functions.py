"""Unit tests for functions.py"""

import pandas as pd
from Row_Eliminator import functions

# allowed_file() tests


def test_allowed_file_csv():
    assert functions.allowed_file("filename.csv")


def test_allowed_file_xls():
    assert functions.allowed_file("filename.xls")


def test_allowed_file_jpg():
    assert not functions.allowed_file("filename.jpg")[0]


def test_allowed_file_csv_jpg():
    assert not functions.allowed_file("filename.csv.jpg")[0]

# upload_file() tests


# read_db() tests

def test_read_db_csv():
    output = functions.read_db('tests/test_db.csv')
    assert isinstance(output, pd.DataFrame), "Did not return pandas DataFrame"


def test_read_db_xls():
    output = functions.read_db('tests/test_db.xls')
    assert isinstance(output, pd.DataFrame), "Did not return pandas DataFrame"

# def_cols() tests
