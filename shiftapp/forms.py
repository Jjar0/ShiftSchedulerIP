from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import InputRequired, ValidationError

from shiftapp.models import User  # for checking existing usernames

# form used for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])  # username field
    password = PasswordField('Password', validators=[InputRequired()])  # password field
    submit = SubmitField('Login') 

# form used for entering shifts 
class ShiftForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()]) # date field as actual date
    startTime = StringField('Start Time', validators=[InputRequired()])  # start time field
    endTime = StringField('End Time', validators=[InputRequired()])  # end time field
    assignedTo = SelectField('Assign To', coerce=int)  # dropdown for employee assign
    submit = SubmitField('Create Shift') 

# form used to manage employees
class ManageEmployeesForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])  # new username
    password = PasswordField('Password', validators=[InputRequired()])  # new password
    addSubmit = SubmitField('Add Employee') 

    employeeToRemove = SelectField('Select Employee to Remove', coerce=int)  # dropdown of employees
    removeSubmit = SubmitField('Remove Employee')  # removal of user + shifts
    removeShiftsSubmit = SubmitField('Remove All Shifts for Employee')  # keep user but clear shifts

     # block duplicate usernames
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')