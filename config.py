#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :config.py
#@time   :2020/3/1710:49
#@Author :jmgen
#@Version:1.0
#@Desc   :

import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    # DEBUG=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                           'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 6
    SECRET_KEY = 'secret key to protect from csrf'
    WTF_CSRF_SECRET_KEY = 'random key for form'  # for csrf protection

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    # 配置邮箱服务器
    MAIL_SERVER = "smtp.163.com"
    # 配置服务器端口
    MAIL_PORT =465
    # 配置
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # 配置邮箱用户名
    MAIL_USERNAME = ''
    # 配置邮箱密码
    MAIL_PASSWORD = ""
    # 配置数据库
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProdConfig(Config):
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    "development": DevConfig,
    "testing": TestingConfig,
    "production": ProdConfig,
    "default": DevConfig
}

