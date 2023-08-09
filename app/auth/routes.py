from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user

from app.auth import bp
from app.auth.forms import LoginForm, SignUpForm
from app.models import User, db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        # check if the username and password are correct
        if user and user.check_password(password):
            login_user(user)

            return redirect(url_for('main.index'))
        
        else:
            flash("Incorrect username or password!")
            

    return render_template('auth/login.html', form=form)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, email=email)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()

            flash("Account created successfully. You can now login")
            return redirect(url_for('auth.login'))
        else:
            flash("Username already exists. Please choose another one")

    return render_template('auth/signup.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))