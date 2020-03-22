#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :errors.py
#@time   :2020/3/1710:49
#@Author :jmgen
#@Version:1.0
#@Desc   :
from flask import render_template
from .import main

@main.app_errorhandler(403)
def forbidden():
    return render_template("403.html"),403

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@main.app_errorhandler(500)
def internal_server_errors(e):
    return render_template("500.html"),500