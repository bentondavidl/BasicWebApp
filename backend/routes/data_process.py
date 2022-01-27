from flask import Blueprint, render_template, redirect, request, session, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import pandas as pd

from backend import mongo

bp = Blueprint("data_process", __name__)

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            print('file found')
            return parse_file(file)
    return render_template('upload.html')


def parse_file(file: FileStorage):
    return repr(pd.read_csv(file))
