#-*- coding:utf-8 -*-
from app import app, lm
from flask import request, redirect, render_template, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import subprocess32, shlex, json
from .forms import UserForm, UseraddForm, DomainaddForm, DomaindeployForm, TestForm
from .models import User, Domain
import time

def execute(cmd):
    child = subprocess32.Popen(shlex.split(cmd), shell=False)
    child.wait()
    returncode = child.returncode
    return returncode

@lm.user_loader
def load_user(username):
    u = User(username)
    return u

@app.route('/testpost', methods=['POST'])
def testpost():
    time.sleep(3)
    #form = TestForm()
    domain = request.form.get("domain","11")
    #return jsonify(domain)
    return domain

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')
#    cmd = "pwd"
#    child = subprocess32.Popen(cmd, stdout=subprocess32.PIPE, shell=False)
#    #child.wait()
#    out = child.communicate()[0]
#    return render_template('test.html', out=out)

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
    else:
        page = int(page)
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
            test_directory = form.test_directory.data
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
                domain_obj.save(domain, ip, test_directory, directory, c_version, n_version, user, password)
                flash("add domian successfully!", category='success')
                return redirect(request.args.get("next") or url_for("domain"))
            except:
                flash("domain add failed", category='error')
        else:
            flash(u"不能为空", category='error')
    return render_template('domain_add.html', title=u'添加域名', form=form)

@app.route('/domain/edit', methods=['GET', 'POST'])
@login_required
def domain_edit():
    if current_user.username != "admin":
        flash("Permission denied", category='error')
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
            test_directory = form.test_diretory.data
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
                domain_obj.save(domain, ip, test_directory, directory, c_version, n_version, user, password)
                flash("add domian successfully!", category='success')
                return redirect(request.args.get("next") or url_for("domain"))
            except:
                flash("domain add failed", category='error')
        else:
            flash(u"不能为空", category='error')
    return render_template('domain_edit.html', title=u'编辑域名', form=form, domain_dic=domain_dic)

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


@app.route('/domain/deploy', methods=['POST'])
@login_required
def domain_deploy():
    if form.validate_on_submit():
        domain = request.form.get("domain")
        action = request.form.get("action")
        cmd = "pwd"
        child = subprocess32.Popen(cmd, stdout=subprocess32.PIPE, shell=False)
        home = child.communicate()[0]
	#回滚
        if action == 1:
            version = request.form.get("version")
            domain_dic = Domain.find_one(domain)
            n_version = domain_dic['n_version']
            directory = domain_dic['directory']
            test_directory = domain_dic['test_directory']
            ip = domain_dic['ip']
            user = domain_dic['user']
            password = domain_dic['password']
            if version >= n_version:
                return u'版本号错误'
            cmd = "cd " + test_directory + "&& git checkout " domain + "-" + version + " && bash " + home + "/app/scripts/auto_rsync.sh " + test_directory + " " + directory + " " + ip + " " + user + " " + password
            returncode = execute(cmd)
            if returncode == 0:
                Domain.update(domain, ip, test_directory, directory, version, n_version, user, password)
                return u"成功"
            else:
                return u"失败"
        #部署最新
        elif action == 0:
            n_version = Domain.find_one(domain)['n_version']
            version = n_version + 1
            cmd = "bash app/scripts/auto_rsync.sh " + test_directory + " " + directory + " " + ip + " " + user + " " + password
            returncode = execute(cmd)
            if returncode == 0:
                Domain.update(domain, ip, test_directory, directory, version, version, user, password)
                tag_cmd = "cd " + test_directory + " && git tag " + domain + "-" + version
                tag_code = execute(tag_cmd)
                return u"成功"
            else:
                return u"失败"
        else:
            return u"fuck you"

