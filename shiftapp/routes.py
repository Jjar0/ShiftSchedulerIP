from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from shiftapp import app, db
from shiftapp.models import User, Shift
from shiftapp.forms import LoginForm, ShiftForm, AddEmployeeForm, RemoveEmployeeForm

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
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('home'))

    # init two separate forms
    addForm = AddEmployeeForm()
    removeForm = RemoveEmployeeForm()

    # set dropdown choices for removal form BEFORE validation
    employees = User.query.filter_by(role='employee').all()
    removeForm.employeeToRemove.choices = [(emp.id, emp.username) for emp in employees]

    # add employee
    if addForm.addSubmit.data and addForm.validate_on_submit():
        print("Trying to add:", addForm.username.data)  # debug line for adding attempt
        newEmp = User(username=addForm.username.data, password=addForm.password.data, role='employee')
        db.session.add(newEmp)
        db.session.commit()
        flash('Employee added.')
        return redirect(url_for('manageEmployees'))
    
    # remove all shifts
    elif removeForm.removeShiftsSubmit.data and removeForm.validate_on_submit():
        Shift.query.filter_by(assignedTo=removeForm.employeeToRemove.data).delete()
        db.session.commit()
        flash('Shifts removed for employee.')
        return redirect(url_for('manageEmployees'))

    # remove employee + shifts
    elif removeForm.removeSubmit.data and removeForm.validate_on_submit():
        Shift.query.filter_by(assignedTo=removeForm.employeeToRemove.data).delete()
        toDelete = User.query.get(removeForm.employeeToRemove.data)
        db.session.delete(toDelete)
        db.session.commit()
        flash('Employee and their shifts removed.')
        return redirect(url_for('manageEmployees'))

    # debug print: show current list of employees
    print("Current employees:", [u.username for u in employees])

    # return page with both forms
    return render_template('manage_employees.html', addForm=addForm, removeForm=removeForm)

# logout current user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
