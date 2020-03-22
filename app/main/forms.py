#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :forms.py
#@time   :2020/3/1710:49
#@Author :jmgen
#@Version:1.0
#@Desc   :
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField
from wtforms.validators import DataRequired,Length,Email

class CommentForm(FlaskForm):
    name=StringField(u"标题",validators=[DataRequired()])
    email=StringField(u"邮箱",validators=[DataRequired(),Length(1.64),Email()])
    content=TextAreaField(u'内容', validators=[DataRequired(), Length(1, 1024)])
    follow=StringField(validators=[DataRequired()])