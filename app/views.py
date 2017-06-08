#-*- coding:utf-8 -*-
from app import app, lm, db
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import subprocess, shlex
#import subprocess32, shlex
from .forms import UserForm, UseraddForm, DomainaddForm, DomaineditForm, DomaindeployForm
from .models_sql import User, Domain, Log
import time


def r_log(action, result, domain_id=0, f_version=0):
    if current_user.is_authenticated:
        user_id = int(current_user.id)
    else:
        user_id = 0
    datetime = int(time.time())
    log = Log(user_id=user_id, domain_id=domain_id, f_version=f_version, datetime=datetime, action=action, result=result)
    db.session.add(log)
    db.session.commit()


def execute(cmd, cwd=None):
    child = subprocess.Popen(shlex.split(cmd), cwd=cwd, shell=False)
    #child = subprocess32.Popen(shlex.split(cmd), cwd=cwd, shell=False)
    child.wait()
    returncode = child.returncode
    return returncode

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/test/', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        file = request.files['file']
        file.save("app/static/upload/aa.png")
        return "aa"
    else:
#        page = request.args.get('p')
#        if page == None:
#            page = 1
#        else:
#            page = int(page)
#        pagination = User.query.paginate(page, 10, False)
#        users = pagination.items
#        return render_template('test.html', title='user', users=users, pagination=dir(pagination))
        return render_template('test.html', auth=current_user.is_authenticated, user_id=current_user.get_id())

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get("next") or url_for("log"))
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user != None and check_password_hash(user.password, form.password.data):
        #if user and user.password == form.password.data:
            login_user(user)
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
    if current_user.id != 1:
        flash("Permission denied", category='error')
        return redirect(request.args.get("next") or url_for("login"))
    page = request.args.get('p')
    if page == None:
        page = 1
    else:
        page = int(page)
    pagination = User.query.paginate(page, 10, False)
    users = pagination.items
    return render_template('user.html', title='user', users=users, pagination=pagination)

@app.route('/user/add/', methods=['GET', 'POST'])
@login_required
def user_add():
    if current_user.id != 1:
        flash("Permission denied", category='error')
        r_log("user add deny", 1)
        return redirect(request.args.get("next") or url_for("login"))
    form = UseraddForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            master = form.master.data
            user = User.query.filter_by(username=username).first()
            if user != None:
                flash("The user name is unavailable", category='error')
                r_log("user add", 1)
                return redirect(request.args.get("next") or url_for("user_add"))
            try:
                password_hash = generate_password_hash(password)
                user = User(username=username, master=master, password=password_hash)
                db.session.add(user)
                db.session.commit()
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
    if current_user.id != 1:
        flash("Permission denied", category='error')
        r_log("user del deny", 1)
        return redirect(request.args.get("next") or url_for("login"))
    id = int(request.args.get('u'))
    if id == 1:
        flash(u"不可删除", category='error')
        return redirect(request.args.get("next") or url_for("user"))
    try:
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
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
    form = UsersetForm()
    id = request.args.get('u')
    if id == None:
        id = 0
        name = ""
        master = ""
    else:
        user = User.query.filter_by(id=id).first()
        name = user.username
        master = user.master
    if request.method == 'POST':
        if form.validate_on_submit():
            id = int(form.id.data)
            master = form.master.data
            password = form.password.data
            user = User.query.filter_by(id=id).first()
            if user == None:
                flash("User not exist", category='error')
                r_log("user setting", 1)
                return redirect(request.args.get("next") or url_for("user"))
            try:
                password_hash = generate_password_hash(password)
                user.master = master
                user.password = password_hash
                db.session.add(user)
                db.session.commit()
                r_log("user setting", 0)
                flash("successfully!", category='success')
                return redirect(request.args.get("next") or url_for("user"))
            except:
                flash(u"更新失败", category='error')
                r_log("user setting", 1)
        else:
            flash(u"不能为空", category='error')
            r_log("user setting", 1)
    return render_template('user_settings.html', title='settings', form=form, id=id, name=name, master=master)

@app.route('/log/', methods=['GET', 'POST'])
@login_required
def log():
    page = request.args.get('p')
    if page == None:
        page = 1
    else:
        page = int(page)
    pagination = Log.query.paginate(page, 10, False)
    logs = pagination.items
    return render_template('log.html', title='log', pagination=pagination, logs=logs)

@app.route('/domain/', methods=['GET', 'POST'])
@login_required
def domain():
    page = request.args.get('p')
    if page == None:
        page = 1
    else:
        page = int(page)
    pagination = Domain.query.paginate(page, 10, False)
    domains = pagination.items
    return render_template('domain.html', title=u'域名', domains=domains, pagination=pagination)

@app.route('/domain/add/', methods=['GET', 'POST'])
@login_required
def domain_add():
    if current_user.id != 1:
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
            domain_obj = Domain.query.filter_by(domain=domain).first()
            if domain_obj != None:
                flash("The domain is repetitive", category='error')
                r_log("domain add", 1)
                return redirect(request.args.get("next") or url_for("domain_add"))
            try:
                domain = Domain(domain=domain, ip=ip, test_directory=test_directory, directory=directory, c_version=c_version, n_version=n_version, user=user, password=password)
                db.session.add(domain)
                db.session.commit()
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
    if current_user.id != 1:
        flash("Permission denied", category='error')
        r_log("domain edit deny", 1)
        return redirect(request.args.get("next") or url_for("login"))
    form = DomaineditForm()
    id = request.args.get('d')
    if id == None:
        id = 0
        domain_dic = {}
    else:
        domain_dic = Domain.query.filter_by(id=id).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            id = form.domain.id
            #domain = form.domain.data
            ip = form.ip.data
            test_directory = form.test_directory.data
            directory = form.directory.data
            #c_version = form.c_version.data
            #n_version = form.n_version.data
            user = form.user.data
            password = form.password.data
            domain_obj = Domain.query.filter_by(id=id).first()
            if domain_obj == None:
                flash("Domain not exist", category='error')
                r_log("Domain edit", 1)
                return redirect(request.args.get("next") or url_for("domain"))
            try:
                domain_obj.ip = ip
                domain_obj.test_directory = test_directory
                domain_obj.directory = directory
                domain_obj.user = user
                domain_obj.password = password
                db.session.add(domain_obj)
                db.session.commit()
                flash("edit domian successfully!", category='success')
                r_log("domain edit", 0)
                return redirect(request.args.get("next") or url_for("domain"))
            except:
                flash("domain edit failed", category='error')
                r_log("domain edit", 1)
        else:
            flash(u"不能为空", category='error')
            r_log("domain edit", 1)
    return render_template('domain_edit.html', title=u'编辑域名', form=form, domain_dic=domain_dic)

@app.route('/domain/del/', methods=['GET', 'POST'])
@login_required
def domain_del():
    if current_user.id != 1:
        flash("Permission denied", category='error')
        r_log("domain del deny", 0)
        return redirect(request.args.get("next") or url_for("login"))
    id = request.args.get('d')
    try:
        domain = Domain.query.filter_by(id=id).first()
        db.session.delete(domain)
        db.session.commit()
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
    id = request.form.get("domain")
    action = int(request.form.get("action"))
    domain = Domain.query.filter_by(id=id).first()
    c_version = int(domain.c_version)
    n_version = int(domain.n_version)
    directory = domain.directory
    test_directory = domain.test_directory
    ip = domain.ip
    user = domain.user
    password = domain.password

    #回滚
    if action == 1:
        version = int(request.form.get("version"))
        if version >= n_version:
            r_log("rollback", 1)
            return u'版本号错误'
        cmd1 = "git checkout " + str(id) + "-" + str(version)
        cmd2 = "bash app/scripts/auto_rsync.sh " + test_directory + " " + directory + " " + ip + " " + user + " " + password
        returncode1 = execute(cmd1, test_directory)
        returncode2 = execute(cmd2)
        if returncode1 == 0 and returncode2 == 0:
            domain.c_version = version
            db.session.add(domain)
            db.session.commit()
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
            cmd1 = "git checkout " + str(id) + "-" + str(n_version)
            returncode1 = execute(cmd1, test_directory)
        version = str(n_version + 1)
        cmd2 = "bash app/scripts/auto_rsync.sh " + test_directory + " " + directory + " " + ip + " " + user + " " + password
        returncode2 = execute(cmd2)
        if returncode1 == 0 and returncode2 == 0:
            domain.c_version = version
            domain.n_version = version
            db.session.add(domain)
            db.session.commit()
            tag_cmd = "git tag " + str(id) + "-" + version
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

