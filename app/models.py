#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :models.py
#@time   :2020/3/1710:49
#@Author :jmgen
#@Version:1.0
#@Desc   :
import hashlib
from datetime import datetime
from werkzeug.security import  generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import db,login_manager

class User(UserMixin,db.Model):
    __tablename__ = "user"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True,index=True)
    username=db.Column(db.String(64),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    avatar_hash=db.Column(db.String(32))

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is not None:
            self.avatar_hash=hashlib.md5(self.email.encode("utf-8")).hexdigest()

    @staticmethod
    def insert_admin(email,username,password):
        user=User(email=email,username=username,password=password)
        db.session.add(user)
        db.session.commit()

    @property
    def password(self):
        raise ArithmeticError(u"密码不可读")

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def gravatar(self, size=40, default='identicon', rating='g'):
        url = 'https://gravatar.loli.net/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()

        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class BlogInfo(db.Model):
    __tablename__="blog_info"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(64))
    signature=db.Column(db.Text)
    navbar=db.Column(db.String(64))

    @staticmethod
    def insert_blog_info():
        blog_info=BlogInfo(title=u'开源博客系统',signature=u'让每个人都轻松拥有可管理的个人博客！',navbar='inverse')
        db.session.add(blog_info)
        db.session.commit()

class BlogView(db.Model):
    __tablename__="blog_view"
    id=db.Column(db.Integer,primary_key=True)
    num_of_view=db.Column(db.BigInteger,default=0)

    @staticmethod
    def insert_view():
        view=BlogView(num_of_view=0)
        db.session.add(view)
        db.session.commit()

    @staticmethod
    def add_view(db):
        view=BlogView.query.first()
        if view is not None:
            view.num_of_view += 1
            db.session.add(view)
            db.session.commit()
        else:
            id=1
            num_of_view=1
            view=BlogView(id=id,num_of_view=num_of_view)
            db.session.add(view)
            db.session.commit()

class Article(db.Model):
    __tablename__="articles"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(64),unique=True)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    num_of_view = db.Column(db.Integer, default=0)

    @staticmethod
    def add_view(article, db):
        article.num_of_view += 1
        db.session.add(article)
        db.session.commit()
