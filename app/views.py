#-*- coding:utf-8 -*-
from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import subprocess32, shlex
from .forms import UserForm, UseraddForm, DomainaddForm, DomaindeployForm
from .models import User, Domain

@lm.user_loader
def load_user(username):
    u = User(username)
    return u

@app.route('/test')
def test():
    config = app.config['SECRET_KEY']
    return render_template('test.html', users=config)

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
    else:
        page = int(page)
    users, count = User.find(10, page)
    return render_template('user.html', title='user', users=users, page=page, count=count)

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
        master = ""
    else:
        master = User.find_one(name)['master']
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            master = form.master.data
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
    return render_template('user_settings.html', title='settings', form=form, name=name, master=master)

@app.route('/log', methods=['GET', 'POST'])
@login_required
def log():
    return render_template('log.html')

@app.route('/domain', methods=['GET', 'POST'])
@login_required
def domain():
    #if current_user.username != "admin":
    #    flash("Permission denied", category='error')
    #    return redirect(request.args.get("next") or url_for("login"))
    page = request.args.get('p')
    if page == None:
        page = 1
    domains = Domain.find(10, page)
    return render_template('domain.html', title=u'域名', domains=domains)

@app.route('/domain/add', methods=['GET', 'POST'])
@login_required
def domain_add():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
        return redirect(request.args.get("next") or url_for("login"))
    form = DomainaddForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            domain = form.domain.data
            ip = form.ip.data
            directory = form.directory.data
            c_version = form.c_version.data
            n_version = form.n_version.data
            user = form.user.data
            password = form.password.data
            domain_obj = Domain(domain)
            if Domain.find_one(domain):
                flash("The domain is repetitive", category='error')
                return redirect(request.args.get("next") or url_for("domain_add"))
            try:
                domain_obj.save(domain, ip, directory, c_version, n_version, user, password)
                flash("add domian successfully!", category='success')
                return redirect(request.args.get("next") or url_for("domain"))
            except:
                flash("domain add failed", category='error')
        else:
            flash(u"不能为空", category='error')
    return render_template('domain_add.html', title=u'添加域名', form=form)

@app.route('/domain/add', methods=['GET', 'POST'])
@login_required
def domain_edit():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
        return redirect(request.args.get("next") or url_for("login"))
    form = DomainaddForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            domain = form.domain.data
            ip = form.ip.data
            directory = form.directory.data
            c_version = form.c_version.data
            n_version = form.n_version.data
            user = form.user.data
            password = form.password.data
            domain_obj = Domain(domain)
            if Domain.find_one(domain):
                flash("The domain is repetitive", category='error')
                return redirect(request.args.get("next") or url_for("domain_add"))
            try:
                domain_obj.save(domain, ip, directory, c_version, n_version, user, password)
                flash("add domian successfully!", category='success')
                return redirect(request.args.get("next") or url_for("domain"))
            except:
                flash("domain add failed", category='error')
        else:
            flash(u"不能为空", category='error')
    return render_template('domain_add.html', title=u'添加域名', form=form)

@app.route('/domain/del', methods=['GET', 'POST'])
@login_required
def domain_del():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
        return redirect(request.args.get("next") or url_for("login"))
    domain = request.args.get('d')
    try:
        Domain.remove(domain)
        flash("user delete successfully!", category='success')
        return redirect(request.args.get("next") or url_for("domain"))
    except:
        flash("Users delete failed", category='error')
        return redirect(request.args.get("next") or url_for("domain"))


@app.route('/domain/deploy', methods=['GET', 'POST'])
@login_required
def domain_deploy():
    form = DomaindeployForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            action = form.action.data
            if action == 1:
                domain = form.domain.data
                n_version = Domain.find_one(domain)['n_version']
                version = form.version.data
                if version >= n_version:
                    return u'版本号错误'
                cmd = "cd && git checkout -b version && git checkout version && rsync "
                child = subprocess32.Popen(shlex.split(cmd), shell=False)
                child.wait()
                returncode = child.returncode
                if returncode == 0:
                    Domain.update()
                    return u"成功"
                else:
                    return u"失败"
            elif action == 0:
                domain = form.domain.data
                n_version = Domain.find_one(domain)['n_version']
                cmd = "git checkout -b version && git checkout version && rsync "
                child = subprocess32.Popen(shlex.split(cmd), shell=False)
                child.wait()
                returncode = child.returncode
                if returncode == 0:
                    Domain.update()
                    return u"成功"
                else:
                    return u"失败"
            else:
                return u"fuck you"

