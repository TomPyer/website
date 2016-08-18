# coding:utf-8
#!/usr/bin/python

from flask import request
from flask import session, redirect, url_for, escape, flash
from flask import render_template
from flask import Flask
from models.u_user import User
from models.t_usertext import Usertext
from models.t_textstatus import TextStatus
import datetime

app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/welecome',methods=['GET','POST'])
def welecome():
    if request.method == 'GET':
        return render_template('welecome.html')
    else:
        return render_template('welecome.html')
@app.route('/search')
def search():
    a = request.values.get('search_body')
    print a
    b = Usertext.query.endswith(a).all()
    #sql = "SELECT * FROM Usertext WHERE find_in_set(a, text);"
    print b
    return redirect(url_for('welecome'))

@app.route('/add_body')
def add_body():
    try:
        a = request.values.get('add_text')
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        t = Usertext(user=session['username'],text=a,createtime=nowtime)
        Usertext.inset(t)
        s = TextStatus(textcode=session['username'],forward=0,forwardUser=None,comment=0,commentUser=None,likes=0,likesUser=None,collection=0,collectionUser=None)
        TextStatus.inset(s)
        print a
        return render_template('welecome.html',search_body=a)
    except:
        return redirect(url_for('welecome'))

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
    try:
        if request.method == 'GET':
            if session['username']:
                return redirect(url_for('welecome'))
            else:
                return render_template('login.html')
    except:
        return render_template('login.html')
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            a={'username':'','password':'','email':'','phone':'',}
            try:
                u = User.query.filter_by(username = request.form['username']).first()
                if u.password == request.form['password']:
                    session['username']= request.form['username']
                    return redirect(url_for('welecome'))
            except Exception,e:
                print 'fail %s'%e
            return render_template('login.html',logging='Username or Password error...')
        else:
            return render_template('login.html',logging='Username or Password is none...')

@app.route('/logout',methods=['GET','POST'])
def logout():
    if request.method == 'GET':
        session.pop('username',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run()
