#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :manage.py
#@time   :2020/3/1710:49
#@Author :jmgen
#@Version:1.0
#@Desc   :

from app import create_app,db
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
from app.models import User,BlogInfo,BlogView

app=create_app('default')
manager=Manager(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

app.jinja_env.globals['BlogInfo'] = BlogInfo
app.jinja_env.globals['BlogView'] = BlogView

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User,BlogInfo=BlogInfo,BlogView=BlogView)

# manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
