from flask_login import login_user, login_required, logout_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user exists, hash the supplied password  and
    # compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again!')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the check above passes then user has access to the page
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # returns a user if the email already exists in database
    user = User.query.filter_by(email=email).first()
    
    # redirect back to signup page if user already exists
    if user:
        flash('Email already exists')
        return redirect(url_for('auth.signup'))
    
    # hash the password and create a new user with the form data
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the use to the database
    db.session.add(new_user)
    db.session.commit()



    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))