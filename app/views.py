# -*- coding: utf-8 -*-

#@author:yangsong
from flask import render_template
from app import app


@app.route('/index')
@app.route('/index/<name>')
def index(name=None):
    if name==None:name='index.html'
    return render_template(name, name=name)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/autoupdate',methods=['POST'])
def auto_update():
    os.system('cd /home/project-01/DayandNight/DN01')
    os.system('git reset --hard')
    os.system('git pull origin master')
    print('git pull finish')
    os.system('service dn01 start')
    os.system('service nginx restart')
    return 'hello webhook'