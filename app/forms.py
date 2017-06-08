from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class TestForm(FlaskForm):

    domain = StringField('Username', validators=[DataRequired()])
    version = StringField('Username', validators=[DataRequired()])
    action = StringField('Username', validators=[DataRequired()])

class UserForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class UsersetForm(FlaskForm):

    id = StringField('id', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    master = StringField('Master', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class UseraddForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    master = StringField('Master', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class DomainaddForm(FlaskForm):
    
    domain = StringField('Domain', validators=[DataRequired()])
    ip = StringField('IP', validators=[DataRequired()])
    test_directory = StringField('test_Directory', validators=[DataRequired()])
    directory = StringField('Directory', validators=[DataRequired()])
    c_version = StringField('c_version', validators=[DataRequired()])
    n_version = StringField('n_version', validators=[DataRequired()])
    user = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class DomaineditForm(FlaskForm):
    
    id = StringField('id', validators=[DataRequired()])
    domain = StringField('Domain', validators=[DataRequired()])
    ip = StringField('IP', validators=[DataRequired()])
    test_directory = StringField('test_Directory', validators=[DataRequired()])
    directory = StringField('Directory', validators=[DataRequired()])
    c_version = StringField('c_version', validators=[DataRequired()])
    n_version = StringField('n_version', validators=[DataRequired()])
    user = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class DomaindeployForm(FlaskForm):

    domain = StringField('Domain', validators=[DataRequired()])
    action = StringField('Action', validators=[DataRequired()])    
    version = StringField('Version')

