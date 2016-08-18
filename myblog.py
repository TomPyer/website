# coding:utf-8
#!/usr/bin/python

from flask import request
from flask import session, redirect, url_for, escape
from flask import render_template
from flask import Flask
from models.u_user import User
app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/welecome',methods=['GET','POST'])
def welecome():
    if request.method =='POST':
        if request.form['texts'] :
            # Search
            body = request.form['text']

    else:
        return render_template('welecome.html')

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/care')
def care():
    return render_template('care.html')

@app.route('/collect')
def collect():
    return render_template('collect.html')

@app.route('/message')
def message():
    return render_template('message.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        a = User.query.filter_by(username=request.form['username']).count()
        b = User.query.filter_by(email = request.form['email']).count()
        c = User.query.filter_by(phone = request.form['phone']).count()
        if a > 0 :
            return render_template('register.html',logging='Username is exist!')
        elif b > 0:
            return render_template('register.html',logging='Email is exist!')
        elif c >0:
            return render_template('register.html',logging='Phone is exist!')
        else:
            u=User(username=request.form['username'],password=request.form['password'],email=request.form['email'],phone=request.form['phone'])
            re_log= User.inset(u)
            if re_log == 'yes':
                return render_template('welecome.html',username=request.form['username'])
            else:
                pass
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            a={'username':'','password':'','email':'','phone':'',}
            try:
                u = User.query.filter_by(username = request.form['username']).first()
                print type(u)
                print u.password
                if u.password == request.form['password']:
                    session['username']= request.form['username']
                    return render_template('welecome.html')
            except Exception,e:
                print 'fail %s'%e
            return render_template('login.html',logging='Username or Password error...')
        else:
            return render_template('login.html',logging='Username or Password is none...')

@app.route('/logout',methods=['GET','POST'])
def logout():
    if request.method == 'GET':
        session.pop('username',None)
    else:
        return render_template('welecome.html')

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run()
