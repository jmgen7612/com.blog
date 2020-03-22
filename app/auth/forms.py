#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :forms.py
#@time   :2020/3/1710:49
#@Author :jmgen
#@Version:1.0
#@Desc   :
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo,Regexp
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    # username = StringField(u"用户名", validators=[DataRequired(), Length(1, 64)])
    email = StringField(u'电子邮件', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),Email()])
    username = StringField(u'用户名', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               u'用户名必须是字母、数字、点号或者下划线组成')])
    password = PasswordField(u'密码', validators=[
        DataRequired(), EqualTo('password2', message=u'密码必须一致')])
    password2 = PasswordField(u'重复密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱号已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被使用')
