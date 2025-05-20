from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, ValidationError
from shiftapp.models import User  # for checking usernames

# form used for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])  # username field
    password = PasswordField('Password', validators=[InputRequired()])  # password field
    submit = SubmitField('Login')  

# form used for entering shifts 
class ShiftForm(FlaskForm):
    date = StringField('Date', validators=[InputRequired()])
    startTime = StringField('Start Time', validators=[InputRequired()])
    endTime = StringField('End Time', validators=[InputRequired()])
    assignedTo = SelectField('Assign To', coerce=int)
    submit = SubmitField('Create Shift')

# form used to add employees
class AddEmployeeForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])  # new employee username
    password = PasswordField('Password', validators=[InputRequired()])  # new employee password
    addSubmit = SubmitField('Add Employee')

    # stop duplicate usernames
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')

# form to remove employees and shifts
class RemoveEmployeeForm(FlaskForm):
    employeeToRemove = SelectField('Select Employee to Remove', coerce=int)  # dropdown of employees
    removeSubmit = SubmitField('Remove Employee')  # remove user + shifts
    removeShiftsSubmit = SubmitField('Remove All Shifts for Employee')  # only remove shifts
