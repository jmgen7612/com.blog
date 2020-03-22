#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :views.py
#@time   :2020/3/1710:49
#@Author :jmgen
#@Version:1.0
#@Desc   :
from flask import render_template,request,current_app,redirect,url_for,flash
from .import main
from .forms import CommentForm
from ..models import User,BlogView,Article
from .. import db

@main.route("/")
def index():
    BlogView.add_view(db)
    page = request.args.get("page", 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(
        page, per_page=current_app.config['ARTICLES_PER_PAGE'],
        error_out=False)
    articles=pagination.items
    return render_template('index.html', articles=articles,Article=Article,
                           pagination=pagination, endpoint='.index')

@main.route("/article/details/<int:id>",methods=['GET','POST'])
def articleDetails(id):
    BlogView.add_view(db)
    form=CommentForm(request.form, follow=-1)
    article=Article.query.get_or_404(id)

    if form.validate_on_submit():
        follow_id=int(form.follow.data)
        if follow_id != -1:
            pass
        return redirect(url_for('.articleDetails', id=article.id, Article=Article, article=article, page=-1))

    page = request.args.get('page', 1, type=int)

    if page==-1:
        pass
    article.add_view(article, db)
    return render_template('article_detials.html', User=User, Article=Article, article=article, page=page,
                           form=form, endpoint='.articleDetails', id=article.id)
