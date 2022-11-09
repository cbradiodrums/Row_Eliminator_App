# Functions for the Row Eliminator App Driver
from flask import Flask, render_template, \
    flash, request
from werkzeug.utils import secure_filename
import os
import pandas as pd
from app import app

ALLOWED_EXTENSIONS = {'csv', 'xls'}


# Check if Allowed File extension
def allowed_file(filename):
    """ In: User Uploaded Filetype, Output: Boolean, .Filetype """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS, \
           filename.rsplit('.', 1)[1].lower()


# Upload File Function
def upload_file():
    """ IN: User File, OUT: User File + Flash Messages """
    if request.method == 'POST':

        # Check if the post request has the file part
        if 'file' not in request.files:
            flash(' ', 'uploads')
            return None

        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No File Selected', 'uploads')
            return None

        # If the user submits a file that is an allowed type:
        if file and allowed_file(file.filename)[0]:
            s_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], s_filename))
            message = flash('File Uploaded', 'uploads')
            return os.path.join(app.config['UPLOAD_FOLDER'], s_filename)

        # If the user submits a that is NOT an allowed type:
        elif not allowed_file(file.filename)[0]:
            flash(f'''Supported File Types: \
                {[str(i).strip('') for i in ALLOWED_EXTENSIONS]}''', 'uploads')
            return None




#  Read in the Uploaded File
def read_db(user_file):  # Reads the file into pandas
    """In: User Uploaded File, Out: Pandas Read of Filetype"""
    flash('File Uploaded', 'uploads')

    if allowed_file(user_file)[1] == 'csv':
        flash(".csv read!", 'file_read')
        return pd.read_csv(user_file)

    elif allowed_file(user_file)[1] == 'xls':
        flash(".xls read!", 'file_read')
        return pd.read_excel(user_file)

    else:
        flash("[Read File] Failed!", 'file_read')
        return None


#  Define and Display Columns for user selection
def def_cols(db_read):
    """ IN: Read User Spreadsheet,
        OUT: Columns flashed in Formbox (Page Display #1) """
    col_sel = []

    for i in range(len(db_read.columns)):
        if len(db_read) > db_read[db_read.columns[i]].nunique() > 1:
            x = f'[{i}]{db_read.columns[i]} -- ' \
                f'{db_read[db_read.columns[i]].nunique()} Unique Values!'
            col_sel.append(x)
            flash(x, 'cols')
    return col_sel  # [i for i in col_sel]


def def_values(db_read, cols_submit):
    """ IN: User Spreadsheet, User Selected Columns
        OUT: Flashed Values for FormBox (Page Display #2) """

    # Enumerate User Selected Columns
    enu_cols = [col[1] for col in cols_submit]

    for col in enu_cols:  # Shows Unique Columns via Flash Formbox
        flash(db_read.columns[int(col)], "message")

        # Display Unique Values Within the Columns via Flash Formbox
        for val in range(len(db_read[db_read.columns[int(col)]].unique())):
            message = f'[{col}] {db_read.columns[int(col)]}' \
                      f' - <{val}> {db_read[db_read.columns[int(col)]].unique()[val]}'
            flash(message, "val")




def row_eliminator_general(db_read, values_submit):
    """ IN: User Spreadsheet, User Selected Offending Values
        OUT: 1) Spreadsheet with only offending value rows
             2) User's Spreadsheet with offending value rows removed """

    # Instantiate Dictionary of User Selected Values
    off_vals = {}
    print("inside FINAL FUNCTION")
    for ov in values_submit:
        off_vals[ov[ov.find("[") + 1:ov.find("]")]] = \
            ov[ov.find('<') + 1:ov.find('>')]

    # Instantiate Copies of db_read to manupulate upon merge
    # Victor = Offending Rows Eliminated, Elimated = Offending Rows
    victor_df, elim_df = db_read.copy(), db_read.copy()

    for col in off_vals:
        for val in off_vals[col]:
            df_drop = db_read[db_read[db_read.columns[int(col)]]
                                 == db_read[db_read.columns[int(col)]].unique()[int(val)]]
            victor_df = (pd.merge(victor_df, df_drop, indicator=True, how='outer')
                         .query('_merge=="left_only"')
                         .drop('_merge', axis=1))
            # df_drop.to_csv(f"./Test_Files/f{val}.csv") #  Incremental Export

    elim_df = (pd.merge(elim_df, victor_df, indicator=True, how='outer')
               .query('_merge=="left_only"')
               .drop('_merge', axis=1))

    # Flash Message for How Many Rows were eliminated with Offending Values
    result = f"{len(elim_df)} Rows Eliminated!! \
     {len(victor_df)} Remaining from initial {len(db_read)}!!"
    flash(result, "error")

    # Upload Files for Download Use
    victor_df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'temp_victor.csv'))
    elim_df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'temp_elim.csv'))

    return True

