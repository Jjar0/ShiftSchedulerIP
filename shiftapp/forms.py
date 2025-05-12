from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

# shift form imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired

# form used for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])  # username field
    password = PasswordField('Password', validators=[InputRequired()])  # password field
    submit = SubmitField('Login')  # submit button

    from wtforms import DateField, TimeField, SelectField

# form used for entering shifts 
class ShiftForm(FlaskForm):
    date = StringField('Date', validators=[InputRequired()])
    startTime = StringField('Start Time', validators=[InputRequired()])
    endTime = StringField('End Time', validators=[InputRequired()])
    assignedTo = SelectField('Assign To', coerce=int)
    submit = SubmitField('Create Shift')