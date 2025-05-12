from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired

# form used for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])  # username field
    password = PasswordField('Password', validators=[InputRequired()])  # password field
    submit = SubmitField('Login')  # submit button

# form used for entering shifts 
class ShiftForm(FlaskForm):
    date = StringField('Date', validators=[InputRequired()])  # date field (as string)
    startTime = StringField('Start Time', validators=[InputRequired()])  # start time field
    endTime = StringField('End Time', validators=[InputRequired()])  # end time field
    assignedTo = SelectField('Assign To', coerce=int)  # dropdown for employee assignment
    submit = SubmitField('Create Shift')  # submit button
