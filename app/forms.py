from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class UseraddForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    master = StringField('Master', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class DomainaddForm(FlaskForm):
    
    domain = StringField('Domain', validators=[DataRequired()])
    ip = StringField('IP', validators=[DataRequired()])
    directory = StringField('Directory', validators=[DataRequired()])
    c_version = StringField('Version', validators=[DataRequired()])
    n_version = StringField('Version', validators=[DataRequired()])
    user = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

