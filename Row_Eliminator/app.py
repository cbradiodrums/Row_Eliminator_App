# Row Eliminator App Driver
from flask import Flask, render_template, redirect, \
    request, url_for, send_file
import functions as func
import os
from glob import glob
from io import BytesIO
from zipfile import ZipFile

app = Flask(__name__)
app_title = 'Row Eliminator'

UPLOAD_FOLDER = './static/uploads/'
TEMPLATES_AUTO_RELOAD = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'DEV'

# Instantiate Empty Files
# test = None
user_file, db_read, db_cols = None, None, None
cols_submit, values_submit = [], []


def create_app():
    @app.route('/')
    def index():
        return render_template('base.html', title='About')

    @app.route('/app', methods=['GET', 'POST'])
    def general_use():
        """ -- Constant Page Refresh Function --
            User Input: Valid .csv or .xls spreadsheet
            Page Display: 1): Columns within User's spreadsheet
                          2) Offending Values within User's Column Selection
            Page Output: 1) Spreadsheet with only offending value rows
                         2) User's Spreadsheet with offending value rows removed """

        # Instantiate Global Variables
        global user_file, db_read, db_cols, \
            cols_submit, values_submit
        page_output = False

        # Determine if User uploaded a valid spreadsheet file
        user_file = func.upload_file()
        if user_file is not None:
            db_read = func.read_db(user_file)

        # Page Display: 1): Columns within User's spreadsheet
        if db_read is not None:
            db_cols = func.def_cols(db_read)

        # Page Display: 2) All Values within User's Column Selection
        if len(cols_submit) == 0:
            cols_submit = request.form.getlist('cols_submit')
        if len(cols_submit) > 0:
            func.def_values(db_read, cols_submit)

        # User selects Offending Values to return Page Output #1 and #2:
        if len(values_submit) == 0:
            values_submit = request.form.getlist('off_values')
        if len(values_submit) > 0:
            page_output = func.row_eliminator_general(db_read, values_submit)

        # Verify Print Block
        print(f'user_file: {user_file}\n '
              f'db_read: {db_read}\n db_cols: {db_cols}\n'
              f'cols_submit: {cols_submit}, values_submit: {values_submit}\n'
              f'page_output: {page_output}\n')

        if page_output:
            # Redirect User to Download Page
            return redirect(url_for('download'))  # Download Clause

        return render_template('app.html', title='General Use')

    @app.route('/hydrocorp')  # Specifically for Hydrocorp functions
    def hydrocorp():
        return render_template('base.html', title='Hydrocorp')

    @app.route('/download')
    def download():
        # target = 'dir1/dir2'

        stream = BytesIO()
        with ZipFile(stream, 'w') as zf:
            for file in glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.csv')):
                zf.write(file, os.path.basename(file))
        stream.seek(0)

        return send_file(
            stream,
            as_attachment=True,
            download_name='archive.zip'
        )

    def reset():
        return redirect(url_for('app'))

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
