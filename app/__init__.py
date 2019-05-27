# -*- coding: utf-8 -*-

#@author:yangsong

from flask import Flask
from sqlalchemy import create_engine
app = Flask(__name__)

from app import views
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

#mysql 配置信息

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'A1@2019@me'
HOST = 'cdb-q1mnsxjb.gz.tencentcdb.com'
PORT = '10102'
DATABASE = 'DayandNight'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
)

db = create_engine(SQLALCHEMY_DATABASE_URI)

from app import api
