from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from shiftapp import app, db
from shiftapp.models import User
from shiftapp.forms import LoginForm

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Replace with hash check later
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('adminDashboard'))
            else:
                return redirect(url_for('employeeDashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html', form=form)
