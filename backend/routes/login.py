from flask import Blueprint, render_template, redirect, request, session
import bcrypt

from backend import mongo

bp = Blueprint("login", __name__)

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = mongo.db['users']
        email = request.form.get('email')
        password = request.form.get('password')

        if request.form.get('register_button'):
            if users.find_one({'email': email}) is None:
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
                users.insert_one({'email': email, 'password': hashed})
                session['user'] = email 
                return 'registered'
            return 'user already exists'

        if request.form.get('login_button'):
            user = users.find_one({'email': email})
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                session['user'] = user['email']
                return redirect('/')
            return 'login failed'

    return render_template('login.html')