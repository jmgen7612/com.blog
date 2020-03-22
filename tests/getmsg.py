#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@file   :getmsg.py
#@time   :2020/3/1716:30
#@Author :jmgen
#@Version:1.0
#@Desc   :

from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/getMsg": {"origins": "*"}})

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getMsg',methods=['GET','POST'])
def home():
    response = {
        ##这里面填写和后台交互的代码
        'mesg': '哈哈，终于调通了 !'
    }
    return jsonify(response)

##启动运行
if __name__ == '__main__':
    app.run()