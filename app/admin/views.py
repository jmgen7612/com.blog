#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :views.py
#@time   :2020/3/1710:49
#@Author :jmgen
#@Version:1.0
#@Desc   :
import sys
import importlib
importlib.reload(sys)

from datetime import datetime
import json
from flask import render_template,redirect,flash,url_for,request,current_app,jsonify
from flask_login import login_required
from . import admin
from ..models import Article,BlogInfo
from .forms import SubmitArticlesForm,ManageArticlesForm,DeleteArticleForm,DeleteArticlesForm,CustomBlogInfoForm
from .. import db

@admin.route('/')
@login_required
def manager():
    return redirect(url_for("admin.custom_blog_info"))

@admin.route('/submit/articles',methods=['GET','POST'])
@login_required
def submitArticles():
    form=SubmitArticlesForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        summary = form.summary.data
        article = Article(title=title, content=content, summary=summary)
        db.session.add(article)
        db.session.commit()
        flash(u'发表博文成功！', 'success')
        article_id = Article.query.filter_by(title=title).first().id
        return redirect(url_for('main.articleDetails', id=article_id))

    if form.errors:
        flash(u'发表博文失败', 'danger')

    return render_template('admin/submit_articles.html', form=form)

@admin.route('/edit/articles/<int:id>',methods=['GET','POST'])
@login_required
def editArticles(id):
    article=Article.query.get_or_404(id)
    form=SubmitArticlesForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        article.summary = form.summary.data
        article.update_time = datetime.utcnow()
        db.session.add(article)
        db.session.commit()
        flash(u'博文更新成功！', 'success')
        return redirect(url_for('main.articleDetails', id=article.id))
    form.title.data = article.title
    form.content.data = article.content
    form.summary.data = article.summary
    return render_template('admin/submit_articles.html', form=form)

@admin.route("/manage/articles",methods=['GET','POST'])
@login_required
def manageArticles():
    form = ManageArticlesForm(request.form)
    form2 = DeleteArticleForm()  # for delete an article
    from3 = DeleteArticlesForm()  # for delete articles

    if form.validate_on_submit():
        page=1
        result=Article.query.order_by(Article.create_time.desc())
        pagination_search=result.paginate(page,per_page=current_app.config['ARTICLES_PER_PAGE'],error_out=False)
    else:
        page=request.args.get('page',1,type=int)
        result = Article.query.order_by(Article.create_time.desc())
        pagination_search = result.paginate(page, per_page=current_app.config['ARTICLES_PER_PAGE'], error_out=False)

    if pagination_search!=0:
        pagination=pagination_search
        articles=pagination_search.items
    else:
        page=request.args.get('page',1,type=int)
        result = Article.query.order_by(Article.create_time.desc())
        pagination=result.paginate(page, per_page=current_app.config['ARTICLES_PER_PAGE'],
                error_out=False)
        articles=pagination.items
    return render_template("admin/manage_articles.html",Article=Article,
                           articles=articles, pagination=pagination,
                           endpoint='admin.manageArticles',
                           form=form, form2=form2, form3=from3,page=page)

@admin.route('/manage/article/delete',methods=['GET','POST'])
@login_required
def deleteArticle():
    form=DeleteArticleForm()
    if form.validate_on_submit():
        articleId=int(form.articleId.data)
        article=Article.query.get_or_404(articleId)
        db.session.delete(article)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'删除失败','danger')
        else:
            flash(u'成功删除博文','success')
    if form.errors:
        flash(u'删除失败','danger')

    return redirect(url_for('admin.manageArticles',page=request.args.get('page', 1, type=int)))

@admin.route('manage/articles/delete',methods=['GET','POST'])
@login_required
def deleteArticles():
    form=DeleteArticlesForm()
    if form.validate_on_submit():
        articleIds=json.loads(form.articleIds.data)
        for articleId in articleIds:
            article = Article.query.get_or_404(articleId)
            db.session.delete(article)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'删除失败', 'danger')
        else:
            flash(u'成功删除博文', 'success')
    if form.errors:
            flash(u'删除失败', 'danger')

    return redirect(url_for('admin.manageArticles', page=request.args.get('page', 1, type=int)))

@admin.route('/manage/bloginfo',methods=['GET','POST'])
@login_required
def customBloginfo():
    form=CustomBlogInfoForm()
    navbars=[(1,u'魅力黑'),(2,u'优雅白')]
    form.navbar.choices=navbars

    if form.validate_on_submit():
        blog=BlogInfo.query.first()
        if blog is not None:
            blog.title = form.title.data
            blog.signature = form.signature.data
            if form.navbar.data == 1:
                blog.navbar = 'inverse'
            if form.navbar.data == 2:
                blog.navbar = 'default'
            db.session.add(blog)
            db.session.commit()
        else:
            title = form.title.data
            signature = form.signature.data
            if form.navbar.data == 1:
                navbar = 'inverse'
            if form.navbar.data == 2:
                navbar = 'default'
            blog=BlogInfo(title=title, signature=signature, navbar=navbar)
            db.session.add(blog)
            db.session.commit()

        flash(u'修改博客基本信息成功')
        return redirect(url_for('admin.customBloginfo'))
    return render_template('admin/custom_blog_info.html', form=form)

@admin.route('/manage/bloginfo/get')
@login_required
def getBloginfo():
    if request.is_xhr:
        blog = BlogInfo.query.first()
        if blog is not None:
            if blog.navbar == 'inverse':
                navbar = 1
            if blog.navbar == 'default':
                navbar = 2
            return jsonify({
                'title': blog.title,
                'signature': blog.signature,
                'navbar': navbar,
            })
        return jsonify({
            "title": "", "signature": "", "navbar": ""
        })

@admin.route('/help')
@login_required
def help():
    return render_template('admin/help_page.html')