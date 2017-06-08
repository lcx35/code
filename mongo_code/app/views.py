#-*- coding:utf-8 -*-
from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import subprocess, shlex
#import subprocess32, shlex
from .forms import UserForm, UseraddForm, DomainaddForm, DomaindeployForm
from .models import User, Domain, Log
import time


def r_log(action, result):
    username = current_user.username
    _id = Log.save(username, action, result)
    return _id

def execute(cmd, cwd=None):
    child = subprocess.Popen(shlex.split(cmd), cwd=cwd, shell=False)
    #child = subprocess32.Popen(shlex.split(cmd), cwd=cwd, shell=False)
    child.wait()
    returncode = child.returncode
    return returncode

@lm.user_loader
def load_user(username):
    u = User(username)
    return u

@app.route('/test/', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        file = request.files['file']
        file.save("app/static/upload/aa.png")
        return "aa"
    else:
        return render_template('test.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get("next") or url_for("log"))
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.find_one(form.username.data)
        if user and User.validate_login(user['password'], form.password.data):
        #if user and user['password'] == form.password.data:
            user_obj = User(form.username.data)
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            r_log("login", 0)
            return redirect(request.args.get("next") or url_for("log"))
        r_log("login", 1)
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/logout/')
def logout():
    r_log("logout", 0)
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/')
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

@app.route('/user/add/', methods=['GET', 'POST'])
@login_required
def user_add():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
        r_log("user add deny", 1)
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
                r_log("user add", 1)
                return redirect(request.args.get("next") or url_for("user_add"))
            try:
                user.save(username, master, password)
                flash("add user successfully!", category='success')
                r_log("user add", 0)
                return redirect(request.args.get("next") or url_for("user"))
            except:
                flash("Wrong username or password!", category='error')
                r_log("user add", 1)
        else:
            flash(u"不能为空", category='error')
            r_log("user add", 1)
    return render_template('user_add.html', title='useradd', form=form)

@app.route('/user/del/', methods=['GET', 'POST'])
@login_required
def user_del():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
        r_log("user del deny", 1)
        return redirect(request.args.get("next") or url_for("login"))
    name = request.args.get('u')
    try:
        User.remove(name)
        flash("user delete successfully!", category='success')
        r_log("user del", 0)
        return redirect(request.args.get("next") or url_for("user"))
    except:
        flash("Users delete failed", category='error')
        r_log("user del", 1)
        return redirect(request.args.get("next") or url_for("user"))

@app.route('/user/settings/', methods=['GET', 'POST'])
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
                r_log("user setting", 1)
                return redirect(request.args.get("next") or url_for("user"))
            try:
                user.update(username, password)
                r_log("user setting", 0)
                flash("successfully!", category='success')
                return redirect(request.args.get("next") or url_for("user"))
            except:
                flash(u"更新失败", category='error')
                r_log("user setting", 1)
        else:
            flash(u"不能为空", category='error')
            r_log("user setting", 1)
    return render_template('user_settings.html', title='settings', form=form, name=name, master=master)

@app.route('/log/', methods=['GET', 'POST'])
@login_required
def log():
    page = request.args.get('p')
    if page == None:
        page = 1
    else:
        page = int(page)
    logs, count = Log.find(10, page)
    return render_template('log.html', title='log', logs=logs, page=page, count=count)

@app.route('/domain/', methods=['GET', 'POST'])
@login_required
def domain():
    page = request.args.get('p')
    if page == None:
        page = 1
    else:
        page = int(page)
    domains, count = Domain.find(10, page)
    return render_template('domain.html', title=u'域名', domains=domains, count=count, page=page)

@app.route('/domain/add/', methods=['GET', 'POST'])
@login_required
def domain_add():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
        r_log("domain add deny", 1)
        return redirect(request.args.get("next") or url_for("login"))
    form = DomainaddForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            domain = form.domain.data
            ip = form.ip.data
            test_directory = form.test_directory.data
            directory = form.directory.data
            c_version = form.c_version.data
            n_version = form.n_version.data
            user = form.user.data
            password = form.password.data
            domain_obj = Domain(domain)
            if Domain.find_one(domain):
                flash("The domain is repetitive", category='error')
                r_log("domain add", 1)
                return redirect(request.args.get("next") or url_for("domain_add"))
            try:
                domain_obj.save(domain, ip, test_directory, directory, c_version, n_version, user, password)
                flash("add domian successfully!", category='success')
                r_log("domain add", 0)
                return redirect(request.args.get("next") or url_for("domain"))
            except:
                flash("domain add failed", category='error')
                r_log("domain add", 1)
        else:
            flash(u"不能为空", category='error')
            r_log("domain add", 1)
    return render_template('domain_add.html', title=u'添加域名', form=form)

@app.route('/domain/edit/', methods=['GET', 'POST'])
@login_required
def domain_edit():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
        r_log("domain edit deny", 1)
        return redirect(request.args.get("next") or url_for("login"))
    form = DomainaddForm()
    domain = request.args.get('d')
    if domain == None:
        domain_dic = {}
    else:
        domain_dic = Domain.find_one(domain)
    if request.method == 'POST':
        if form.validate_on_submit():
            domain = form.domain.data
            ip = form.ip.data
            test_directory = form.test_directory.data
            directory = form.directory.data
            c_version = form.c_version.data
            n_version = form.n_version.data
            user = form.user.data
            password = form.password.data
            domain_obj = Domain(domain)
            try:
                domain_obj.update(domain, ip, test_directory, directory, c_version, n_version, user, password)
                flash("add domian successfully!", category='success')
                r_log("domain edit", 0)
                return redirect(request.args.get("next") or url_for("domain"))
            except:
                flash("domain add failed", category='error')
                r_log("domain edit", 1)
        else:
            flash(u"不能为空", category='error')
            r_log("domain edit", 1)
    return render_template('domain_edit.html', title=u'编辑域名', form=form, domain_dic=domain_dic)

@app.route('/domain/del/', methods=['GET', 'POST'])
@login_required
def domain_del():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
        r_log("domain del deny", 0)
        return redirect(request.args.get("next") or url_for("login"))
    domain = request.args.get('d')
    try:
        Domain.remove(domain)
        flash("user delete successfully!", category='success')
        r_log("domain del", 0)
        return redirect(request.args.get("next") or url_for("domain"))
    except:
        flash("Users delete failed", category='error')
        r_log("domain del", 1)
        return redirect(request.args.get("next") or url_for("domain"))


@app.route('/domain/deploy/', methods=['POST'])
@login_required
def domain_deploy():
    domain = request.form.get("domain")
    action = int(request.form.get("action"))
    domain_dic = Domain.find_one(domain)
    c_version = int(domain_dic['c_version'])
    n_version = int(domain_dic['n_version'])
    directory = domain_dic['directory']
    test_directory = domain_dic['test_directory']
    ip = domain_dic['ip']
    user = domain_dic['user']
    password = domain_dic['password']

    #回滚
    if action == 1:
        version = int(request.form.get("version"))
        if version >= n_version:
            r_log("rollback", 1)
            return u'版本号错误'
        cmd1 = "git checkout " + domain + "-" + str(version)
        cmd2 = "bash app/scripts/auto_rsync.sh " + test_directory + " " + directory + " " + ip + " " + user + " " + password
        returncode1 = execute(cmd1, test_directory)
        returncode2 = execute(cmd2)
        if returncode1 == 0 and returncode2 == 0:
            Domain.update(domain, ip, test_directory, directory, version, n_version, user, password)
            flash("rollback successfully!", category='success')
            r_log("rollback", 0)
            return u"成功"
        else:
            flash("rollback failed", category='error')
            r_log("rollback", 1)
            return u"失败"
    #部署最新
    elif action == 0:
        returncode1 = 0
        if c_version < n_version:
            cmd1 = "git checkout " + domain + "-" + str(n_version)
            returncode1 = execute(cmd1, test_directory)
        version = str(n_version + 1)
        cmd2 = "bash app/scripts/auto_rsync.sh " + test_directory + " " + directory + " " + ip + " " + user + " " + password
        returncode2 = execute(cmd2)
        if returncode1 == 0 and returncode2 == 0:
            Domain.update(domain, ip, test_directory, directory, version, version, user, password)
            tag_cmd = "git tag " + domain + "-" + version
            tag_code = execute(tag_cmd, test_directory)
            flash("deploy successfully!", category='success')
            r_log("deploy", 0)
            return u"成功"
        else:
            flash("deploy failed", category='error')
            r_log("deploy", 1)
            return u"失败"
    else:
        return u"fuck you"

