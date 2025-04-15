from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Имя', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[InputRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[InputRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
