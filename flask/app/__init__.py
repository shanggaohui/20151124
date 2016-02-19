
from flask import Flask
app = flask(__name__)  #创建Flask application对象
from app import views  #引入视图
