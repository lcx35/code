from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import UserForm, UseraddForm
from .models import User

@lm.user_loader
def load_user(username):
    u = User(username)
#    if not u:
#        return None
    return u

@app.route('/test')
def test():
    users = User.find(10, 1)
    return render_template('test.html', users=users)

@app.route('/', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.find_one(form.username.data)
#        if user and User.validate_login(user['password'], form.password.data):
        if user and user['password'] == form.password.data:
            user_obj = User(form.username.data)
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("log"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    return render_template('user.html')

@app.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    return render_template('user_add.html')

@app.route('/user/del', methods=['GET', 'POST'])
@login_required
def user_del():
    return 

@app.route('/user/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    return render_template('user_settings.html')

@app.route('/log', methods=['GET', 'POST'])
@login_required
def log():
    return render_template('log.html')

@app.route('/domain', methods=['GET', 'POST'])
@login_required
def domain():
    return render_template('domain.html')

@app.route('/domain/add', methods=['GET', 'POST'])
@login_required
def domain_add():
    return render_template('domain_add.html')

@app.route('/domain/del', methods=['GET', 'POST'])
@login_required
def domain_del():
    return render_template('log.html')



