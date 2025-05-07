from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from shiftapp import app, db
from shiftapp.models import User
from shiftapp.forms import LoginForm

# redirect root to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # find user by username
        user = User.query.filter_by(username=form.username.data).first()
        # check password
        if user and user.password == form.password.data:
            login_user(user)
            # redirect based on role
            if user.role == 'admin':
                return redirect(url_for('adminDashboard'))
            else:
                return redirect(url_for('employeeDashboard'))
        else:
            flash('Invalid credentials')  # show error message
    return render_template('login.html', form=form)

# admin dashboard
@app.route('/admin')
@login_required
def adminDashboard():
    return render_template('admin.html')

# employee dashboard
@app.route('/employee')
@login_required
def employeeDashboard():
    return render_template('employee.html')
