#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :forms.py
#@time   :2020/3/1710:49
#@Author :jmgen
#@Version:1.0
#@Desc   :
from flask_wtf import FlaskForm
from wtforms import SelectField,StringField,TextAreaField
from wtforms.validators import DataRequired,Length

class SubmitArticlesForm(FlaskForm):
    title = StringField(u'标题', validators=[DataRequired(), Length(1, 64)])
    content = TextAreaField(u'博文内容', validators=[DataRequired()])
    summary = TextAreaField(u'博文摘要', validators=[DataRequired()])

class ManageArticlesForm(FlaskForm):
    pass

class DeleteArticleForm(FlaskForm):
    articleId = StringField(validators=[DataRequired()])

class DeleteArticlesForm(FlaskForm):
    articleIds = StringField(validators=[DataRequired()])

class CustomBlogInfoForm(FlaskForm):
    title = StringField(u'博客标题', validators=[DataRequired()])
    signature = TextAreaField(u'个性签名', validators=[DataRequired()])
    navbar = SelectField(u'导航样式', coerce=int, validators=[DataRequired()])