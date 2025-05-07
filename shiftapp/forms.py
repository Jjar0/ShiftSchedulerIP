from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

# form used for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])  # username field
    password = PasswordField('Password', validators=[InputRequired()])  # password field
    submit = SubmitField('Login')  # submit button