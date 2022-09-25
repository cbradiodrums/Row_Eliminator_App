# Functions for the Row Eliminator Site
from flask import flash, request
from werkzeug.utils import secure_filename
import os
import pandas as pd
from . import app

ALLOWED_EXTENSIONS = {'csv', 'xls'}


# Check if Allowed File extension
def allowed_file(filename):
    """Check if file matches filetype criteria

    Args:
        filename (str): path to file

    Returns:
        bool
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS, \
           filename.rsplit('.', 1)[1].lower()


# Upload File Function
def upload_file():
    """Retrieve uploaded file from POST and save to uploads directory"""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return flash(' ', 'uploads')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return flash('No File Selected', 'uploads')
        if file and allowed_file(file.filename)[0]:
            s_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], s_filename))
            return flash('File Uploaded', 'uploads'), \
                   os.path.join(app.config['UPLOAD_FOLDER'], s_filename)
        elif not allowed_file(file.filename)[0]:
            return flash(f'''Supported File Types: \
            {[str(i).strip('') for i in ALLOWED_EXTENSIONS]}''' \
                         , 'uploads')
    flash('', 'uploads')


#  Read in the Uploaded File
def read_db(db_file: str) -> pd.DataFrame:
    """Reads the file into pandas

    Args:
        db_file (str): File to load into Pandas dataframe

    Returns:
        pd.DataFrame
    """

    if allowed_file(db_file)[1] == 'csv':
        return pd.read_csv(db_file)#, \
               #flash(".csv read!", 'file_read')
    elif allowed_file(db_file)[1] == 'xls':
        return pd.read_excel(db_file)#, \
               #flash(".xls read!", 'file_read')
    else:
        flash("[Read File] Failed!",
              'file_read')


#  Define and Display Columns for user selection
def def_cols(df):
    """Define and Display Columns for user selection

    Args:
        df (pd.DataFrame): _description_

    Returns:
        list: _description_
    """
    # -- Select all columns that have offensive values: --
    victor_df, elim_df, col_sel = df.copy(), df.copy(), []
    for i in range(len(df.columns)):
        if len(df) > df[df.columns[i]].nunique() > 1:
            x = f'[{i}]{df.columns[i]} -- ' \
                f'{df[df.columns[i]].nunique()} Unique Values!'
            col_sel.append(x)
            flash(x, 'cols')
    return [i for i in col_sel]
