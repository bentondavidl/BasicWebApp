from flask import Blueprint, render_template, session

bp = Blueprint("index", __name__)


@bp.route('/')
@bp.route('/index')
def index():
    try:
        user = session['user']
    except KeyError:
        user = None
    return render_template('index.html', user=user)
