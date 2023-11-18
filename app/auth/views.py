from flask import flash
from flask import redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from app.auth.forms import RegistrationForm, LoginForm
from app.auth.models import User
from app.auth import db

from app import app

def authenticate_user(username, password):
# Query the database to check if the user exists and the password is correct
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # If the user and password are valid, return the user ID
        return user.id
    else:
        # If authentication fails, return None
        return None

#Gets data from login
@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        # user_id = authenticate_user(form.username.data, form.password.data)

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            flash('Login successful', 'success')
     
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.')
    
    return render_template("auth/login.html", form=form)
        

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# Gets data from registration
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    form = RegistrationForm()
    
    if form.validate_on_submit() and request.method == 'POST':
        user = User(
            username=  form.username.data,
            email = form.email.data,
            password = form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Thanks for registering.')
        return redirect(url_for('login'))

    return render_template("auth/register.html", form=form)


