from flask import Blueprint, render_template, redirect, request, session, url_for, flash, Response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64

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

@bp.route('/plot', methods=['GET', 'POST'])
def plot_route():
    if request.method == 'POST':
        # get equation from form
        equation = request.form['equation']
        try:
            x_range = tuple(float(x) for x in request.form['range'].split(','))
        except ValueError:
            flash('Range should be two comma separated numbers')
            return redirect(request.url)
        data = generate_data(equation, x_range)
        deriv = calculate_deriv(data)
        plot_equation(data,deriv)
        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(plt.gcf()).print_png(pngImage)
        
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        
        return render_template("plot.html", plot=pngImageB64String)

    return render_template('plot.html')


def parse_file(file: FileStorage):
    return repr(pd.read_csv(file))

def generate_data(equation: str, x_range: 'tuple[float,float]'):
    from sympy.utilities.lambdify import lambdify
    import sympy
    sympy_func = sympy.sympify(equation)
    x = sympy.symbols('x')    
    step_size = (x_range[1]-x_range[0])/250
    func = lambdify(x, sympy_func, 'numpy') # returns a numpy-ready function
    xx = np.arange(start=x_range[0],stop=x_range[1],step=step_size)
    yy = func(xx)
    return xx,yy

def calculate_deriv(data: 'tuple[list,list]'):
    x,y = data
    return x[1:],(y[1:]-y[:-1])/(x[1]-x[0])

def plot_equation(data: 'tuple[list,list]', deriv: 'tuple[list,list]'):
    fig, ax = plt.subplots()
    ax.plot(*deriv,label='Derivative')
    ax.plot(*data,label='Data')
    ax.legend()
    # set the x-spine (see below for more info on `set_position`)
    ax.spines['left'].set_position('zero')

    # turn off the right spine/ticks
    ax.spines['right'].set_color('none')
    ax.yaxis.tick_left()

    # set the y-spine
    ax.spines['bottom'].set_position('zero')

    # turn off the top spine/ticks
    ax.spines['top'].set_color('none')
    ax.xaxis.tick_bottom()
