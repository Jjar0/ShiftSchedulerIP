from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from shiftapp import app, db
from shiftapp.models import User, Shift
from shiftapp.forms import LoginForm, ShiftForm, ManageEmployeesForm

# redirect to login page
@app.route('/')
def home():
    return redirect(url_for('login'))

# login page for all users
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # get user by username
        user = User.query.filter_by(username=form.username.data).first()
        # check password matches
        if user and user.password == form.password.data:
            # login user
            login_user(user)
            # redirect based on role
            if user.role == 'admin':
                return redirect(url_for('adminDashboard'))
            else:
                return redirect(url_for('employeeDashboard'))
        else:
            # show error if login fails
            flash('Invalid credentials')
    # return login page with form
    return render_template('login.html', form=form)

# dashboard for employees
@app.route('/employee')
@login_required
def employeeDashboard():
    # get shifts for logged in user
    shifts = Shift.query.filter_by(assignedTo=current_user.id).all()
    # return employee page with shifts
    return render_template('employee.html', shifts=shifts)

# dashboard for admin to view/add shifts
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def adminDashboard():
    form = ShiftForm()
    # populate dropdown
    form.assignedTo.choices = [(user.id, user.username) for user in User.query.filter_by(role='employee')]

    if form.validate_on_submit():
        # get selected employee
        assignedUser = User.query.get(form.assignedTo.data)
        if not assignedUser:
            # error if employee doesnt exist
            flash('Assigned user does not exist.')
            return redirect(url_for('adminDashboard'))

        # get all shifts for date and employee
        existingShifts = Shift.query.filter_by(
            assignedTo=form.assignedTo.data,
            date=form.date.data
        ).all()

        # check for time overlap
        conflict = any(
            not (form.endTime.data <= shift.startTime or form.startTime.data >= shift.endTime)
            for shift in existingShifts
        )

        if conflict:
            # show conflict error
            flash('Shift conflict! Employee already has shift during this time.')
        else:
            # create and save new shift
            newShift = Shift(
                date=form.date.data,
                startTime=form.startTime.data,
                endTime=form.endTime.data,
                assignedTo=form.assignedTo.data
            )
            db.session.add(newShift)
            db.session.commit()
            flash('Shift added.')

    # get all shifts for table display
    shifts = Shift.query.all()
    # return admin dashboard with form and shift list
    return render_template('admin.html', form=form, shifts=shifts)

# remove individual shift by ID
@app.route('/delete_shift/<int:shiftId>', methods=['POST'])
@login_required
def deleteShift(shiftId):
    # find shift or return 404
    shift = Shift.query.get_or_404(shiftId)
    # delete from database
    db.session.delete(shift)
    db.session.commit()
    flash('Shift removed.', 'success')
    # return admin dashboard
    return redirect(url_for('adminDashboard'))

# admin only employee management page
@app.route('/manage_employees', methods=['GET', 'POST'])
@login_required
def manageEmployees():
    # block access if not admin
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('home'))

    # setup form
    form = ManageEmployeesForm()
    # get all employee users for dropdown
    employees = User.query.filter_by(role='employee').all()
    form.employeeToRemove.choices = [(emp.id, emp.username) for emp in employees]

    # add new employee if form submitted
    if form.addSubmit.data:
        if form.validate_on_submit():
            # create new employee
            newEmp = User(username=form.username.data, password=form.password.data, role='employee')
            db.session.add(newEmp)
            db.session.commit()
            flash('Employee added.')
            return redirect(url_for('manageEmployees'))
        else:
            # catch duplicate username error
            for error in form.username.errors:
                flash(error)


    # delete all shifts for selected employee
    if form.removeShiftsSubmit.data and form.employeeToRemove.data:
        # delete all shifts assigned to employee
        Shift.query.filter_by(assignedTo=form.employeeToRemove.data).delete()
        db.session.commit()
        flash('Shifts removed for employee.')
        return redirect(url_for('manageEmployees'))

    # delete selected employee and their shifts
    if form.removeSubmit.data and form.employeeToRemove.data:
        # delete all shifts for employee
        Shift.query.filter_by(assignedTo=form.employeeToRemove.data).delete()
        # delete user
        toDelete = User.query.get(form.employeeToRemove.data)
        db.session.delete(toDelete)
        db.session.commit()
        flash('Employee and their shifts removed.')
        return redirect(url_for('manageEmployees'))

    # return employee management page
    return render_template('manage_employees.html', form=form)

# logout current user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

