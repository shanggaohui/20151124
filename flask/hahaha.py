#-*-coding:utf:8-*-

from flask import Flask
app = Flask(__name__)
@app.route('/')
def user():
    return '哈哈'

if __name__=='__main__':
    app.run(debug=True)
