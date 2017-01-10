#-*- coding:utf-8 -*-
from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import UserForm, UseraddForm
from .models import User

@lm.user_loader
def load_user(username):
    u = User(username)
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
        if user and User.validate_login(user['password'], form.password.data):
        #if user and user['password'] == form.password.data:
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


@app.route('/user')
@login_required
def user():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
        return redirect(request.args.get("next") or url_for("login"))
    page = request.args.get('p')
    if page == None:
        page = 1
    users = User.find(10, page)
    return render_template('user.html', title='user', users=users)

@app.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
        return redirect(request.args.get("next") or url_for("login"))
    form = UseraddForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            master = form.master.data
            user = User(username)
            if User.find_one(username):
                flash("The user name is unavailable", category='error')
                return redirect(request.args.get("next") or url_for("user_add"))
            try:
                user.save(username, master, password)
                flash("add user successfully!", category='success')
                return redirect(request.args.get("next") or url_for("user"))
            except:
                flash("Wrong username or password!", category='error')
        else:
            flash(u"不能为空", category='error')
    return render_template('user_add.html', title='useradd', form=form)

@app.route('/user/del', methods=['GET', 'POST'])
@login_required
def user_del():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
        return redirect(request.args.get("next") or url_for("login"))
    name = request.args.get('u')
    try:
        User.remove(name)
        flash("user delete successfully!", category='success')
        return redirect(request.args.get("next") or url_for("user"))
    except:
        flash("Users delete failed", category='error')
        return redirect(request.args.get("next") or url_for("user"))

@app.route('/user/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    form = UserForm()
    name = request.args.get('u')
    if name == None:
        name = ""
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User(username)
            if not User.find_one(username):
                flash("User not exist", category='error')
                return redirect(request.args.get("next") or url_for("user"))
            try:
                user.update(username, password)
                flash("successfully!", category='success')
                return redirect(request.args.get("next") or url_for("user"))
            except:
                flash(u"更新失败", category='error')
        else:
            flash(u"不能为空", category='error')
    return render_template('user_settings.html', title='settings', form=form, name=name)

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



