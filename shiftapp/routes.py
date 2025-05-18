from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from shiftapp import app, db
from shiftapp.models import User
from shiftapp.forms import LoginForm

# Scheduler form imports
from shiftapp.models import User, Shift
from shiftapp.forms import LoginForm, ShiftForm
from flask_login import current_user

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
            flash('Invalid credentials')  # show error
    return render_template('login.html', form=form)

# employee dashboard
@app.route('/employee')
@login_required
def employeeDashboard():
    # get shifts assigned to the currently logged in user
    shifts = Shift.query.filter_by(assignedTo=current_user.id).all()
    
    # render dashboard, pass the shifts to the template
    return render_template('employee.html', shifts=shifts)

# admin page to add/view shifts
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def adminDashboard():
    form = ShiftForm()
    form.assignedTo.choices = [(user.id, user.username) for user in User.query.filter_by(role='employee')]

    if form.validate_on_submit():
        # Check if assigned user actually exists
        assignedUser = User.query.get(form.assignedTo.data)
        if not assignedUser:
            flash('Assigned user does not exist.')
            return redirect(url_for('adminDashboard'))

        # Check for conflicting shifts
        existingShifts = Shift.query.filter_by(
            assignedTo=form.assignedTo.data,
            date=form.date.data
        ).all()

        conflict = False
        for shift in existingShifts:
            if not (form.endTime.data <= shift.startTime or form.startTime.data >= shift.endTime):
                conflict = True
                break

        if conflict:
            flash('Shift conflict! Employee already has a shift during this time.')
        else:
            # No conflict; safe to add shift
            newShift = Shift(
                date=form.date.data,
                startTime=form.startTime.data,
                endTime=form.endTime.data,
                assignedTo=form.assignedTo.data
            )
            db.session.add(newShift)
            db.session.commit()
            flash('Shift added successfully.')

    shifts = Shift.query.all()
    return render_template('admin.html', form=form, shifts=shifts)