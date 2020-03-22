#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :views.py
#@time   :2020/3/1710:49
#@Author :jmgen
#@Version:1.0
#@Desc   :
import hashlib
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required
from . import auth
from .forms import LoginForm,RegistrationForm
from .. import db
from ..models import User

@auth.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash(u'登陆成功！欢迎回来，%s!' % user.username, 'success')
            next=request.args.get('next')
            if next is None or not next.startwith('/'):
                next=url_for('main.index')
            return redirect(next)
        # elif user is None and user.verify_password(form.password.data):
        #     user=User.query.filter_by(username=form.username.data).first()
        #     login_user(user)
        #     flash(u'登陆成功！欢迎回来，%s!' % user.username, 'success')
        #     next = request.args.get('next')
        #     if next is None or not next.startwith('/'):
        #         next = url_for('main.index')
        #     return redirect(next)
        else:
            flash(u'登陆失败！用户名或密码错误，请重新登陆。', 'danger')
    if form.errors:
        print(form.errors)
        flash(u'登陆失败，请尝试重新登陆.', 'danger')

    return render_template("auth/login.html",form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已退出登陆。', 'success')
    return redirect(url_for('main.index'))

@auth.route("register",methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        avatar_hash=hashlib.md5(form.email.data.encode("utf-8")).hexdigest()
        user=User(email=form.email.data,username=form.username.data,password=form.password.data,avatar_hash=avatar_hash)
        db.session.add(user)
        db.session.commit()
        flash(u'注册成功')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)
