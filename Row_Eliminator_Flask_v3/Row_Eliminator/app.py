from flask import Flask, render_template, redirect, \
    flash, session, request, send_from_directory, \
    url_for, send_file
from werkzeug.utils import secure_filename
import functions as func
import os
import pandas as pd
from flask import send_file
from glob import glob
from io import BytesIO
from zipfile import ZipFile



app = Flask(__name__)
app_title = 'Row Eliminator'

UPLOAD_FOLDER = './static/uploads/'
TEMPLATES_AUTO_RELOAD = True
ALLOWED_EXTENSIONS = {'csv', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'DEV'
db_read, db_cols = None, None

def create_app():
    @app.route('/')
    def index():
        return render_template('base.html', title='About')

    @app.route('/app', methods=['GET', 'POST'])
    def general_use():
        global db_read, db_cols
        current_db = func.upload_file()
        if current_db is not None:
            db_read = func.read_db(str(current_db[1]))
        if db_read is not None:
            db_cols = func.def_cols(db_read[0])
        cols_submit = request.form.getlist('cols_submit')
        enu_cols = [col[1] for col in cols_submit]
        if len(cols_submit) > 0:
            for col in enu_cols:
                flash(db_read[0].columns[int(col)], "message")
                for val in range(len(db_read[0][db_read[0].columns[int(col)]].unique())):
                    message = f'[{col}] {db_read[0].columns[int(col)]}' \
                              f' - <{val}> {db_read[0][db_read[0].columns[int(col)]].unique()[val]}'
                    flash(message, "val")
        off_vals_form = request.form.getlist('off_vals')
        if len(off_vals_form) > 0:
            off_vals = {}
            for ov in off_vals_form:
                off_vals[ov[ov.find("[")+1:ov.find("]")]] = \
                ov[ov.find('<')+1:ov.find('>')]
            victor_df, elim_df = db_read[0].copy(), db_read[0].copy()
            for col in off_vals:
                for val in off_vals[col]:
                    df_drop = db_read[0][db_read[0][db_read[0].columns[int(col)]]
                                         == db_read[0][db_read[0].columns[int(col)]].unique()[int(val)]]
                    victor_df = (pd.merge(victor_df, df_drop, indicator=True, how='outer')
                                 .query('_merge=="left_only"')
                                 .drop('_merge', axis=1))
                    # df_drop.to_csv(f"./Test_Files/f{val}.csv") #  Incremental Export
            elim_df = (pd.merge(elim_df, victor_df, indicator=True, how='outer')
                       .query('_merge=="left_only"')
                       .drop('_merge', axis=1))
            result = f"{len(elim_df)} Rows Eliminated!! \
             {len(victor_df)} Remaining from initial {len(db_read[0])}!!"
            flash(result, "error")
            victor_df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'temp_victor.csv'))
            elim_df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'temp_elim.csv'))
            return redirect(url_for('download')) # Download Clause

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
