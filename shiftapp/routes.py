from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from shiftapp import app, db
from shiftapp.models import User, Shift
from shiftapp.forms import LoginForm, ShiftForm

# Redirect to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Find username
        user = User.query.filter_by(username=form.username.data).first()
        # password
        if user and user.password == form.password.data:
            login_user(user)
            # Redirect on role
            if user.role == 'admin':
                return redirect(url_for('adminDashboard'))
            else:
                return redirect(url_for('employeeDashboard'))
        else:
            flash('Invalid credentials')  # Show error if login fails
    return render_template('login.html', form=form)

# Employee dashboard
@app.route('/employee')
@login_required
def employeeDashboard():
    # Get shifts assigned to logged in user
    shifts = Shift.query.filter_by(assignedTo=current_user.id).all()
    # Render dashboard pass shifts to template
    return render_template('employee.html', shifts=shifts)

# Admin dashboard to add/view shifts
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def adminDashboard():
    form = ShiftForm()
    # Populate dropdown with usernames
    form.assignedTo.choices = [(user.id, user.username) for user in User.query.filter_by(role='employee')]

    if form.validate_on_submit():
        # Check if assigned user exists
        assignedUser = User.query.get(form.assignedTo.data)
        if not assignedUser:
            flash('Assigned user does not exist.')
            return redirect(url_for('adminDashboard'))

        # Check for conflicting shifts on same day
        existingShifts = Shift.query.filter_by(
            assignedTo=form.assignedTo.data,
            date=form.date.data
        ).all()

        # Simple overlap check for time conflicts
        conflict = any(
            not (form.endTime.data <= shift.startTime or form.startTime.data >= shift.endTime)
            for shift in existingShifts
        )

        if conflict:
            flash('Shift conflict! Employee already has a shift during this time.')
        else:
            # No conflict -> safe to add shift
            newShift = Shift(
                date=form.date.data,
                startTime=form.startTime.data,
                endTime=form.endTime.data,
                assignedTo=form.assignedTo.data
            )
            db.session.add(newShift)
            db.session.commit()
            flash('Shift added successfully.')

    # Query shifts to display in admin
    shifts = Shift.query.all()
    return render_template('admin.html', form=form, shifts=shifts)

# Route to remove shifts
@app.route('/delete_shift/<int:shiftId>', methods=['POST'])
@login_required
def deleteShift(shiftId):
    # Find shift by ID or return 404
    shift = Shift.query.get_or_404(shiftId)
    # Delete shift
    db.session.delete(shift)
    db.session.commit()
    flash('Shift removed successfully.', 'success')
    # Redirect
    return redirect(url_for('adminDashboard'))

# Route for logging out :D
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
