from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from app import db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Username not found')
            return redirect('/login')

        if user is not None and not user.check_password(form.password.data):
            flash('Invalid password')
            return redirect('/login')
        
        login_user(user)
        return redirect('/index')

        return redirect('/index')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')


@app.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/index')
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('/login')
    return render_template('register.html', form=form)