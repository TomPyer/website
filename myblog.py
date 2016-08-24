# coding:utf-8
#!/usr/bin/python

from flask import request
from flask import session, redirect, url_for, escape, flash
from flask import render_template
from flask import Flask
from models.u_user import User
from models.t_usertext import Usertext
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/welcome',methods=['GET','POST'])
def welcome():
    '''print User.query.limit(10).all() #查询返回的数据的数目

        data_all=User.query.all()me
        print (data_all)#查询全部

        for i in range(len(data_all)):
         print data_all[i].username+" "+data_all[i].email+" "+data_all[i].phone
    '''
    forward_num = int(0)
    comment_num = int(0)
    likes_num = int(0)
    collect_num = int(0)
    try:
        b = Usertext.query.filter_by(user = session['username']).all()
        c = Usertext.query.filter_by(user = session['username']).count()
        praise_num = 0

        for i in b :
            praise_num += i.likes

        for u in b :
            forward_num += u.forward
            comment_num += u.comment
            likes_num += u.likes
            collect_num += u.collection

        b = b[::-1]

    except Exception,e:
        print e
        f = Usertext.query.all()
        f = f[::-1]
        return render_template('welcome.html',
                               text_info = f,
                               prompt = 'Log in to display personal information.',
                               forward = forward_num,
                               comment = comment_num,
                               likes = likes_num,
                               collection = collect_num,
                               )

    if request.method == 'GET':
        try:
            if session['username']:
                return render_template('welcome.html',
                                       name = session['username'],
                                       text_info = b,
                                       tweets = c,
                                       praise = praise_num,
                                       forward =forward_num,
                                       comment = comment_num,
                                       likes = likes_num,
                                       collection = collect_num,
                                       )
        except:
            return redirect(url_for('login'))
    else:
        return render_template('welcome.html',
                               text_info = b,
                               )


@app.route('/search')
def search():
    a = request.values.get('search_body')
    #sql = "SELECT * FROM Usertext WHERE find_in_set(a, text);"
    #print b
    return redirect(url_for('welcome'))

@app.route('/add_fclc')
def add_fclc():
    re = ''
    t = Usertext()
    a = request.values.get('fclc')
    b = request.values.get('textid')
    text = Usertext.query.filter_by(id=b).first()

    if int(a) == 1 :
        if session['username'] in text.forwardUser :
            return render_template('welcome.html',logging = 'Sorry,You have forwarded this blog.')
        text.forward += 1
        text.forwardUser += session['username']
        re = t.commit()
    if int(a) == 2:
        pass
    if int(a) == 3:
        if session['username'] in text.likesUser:
            return render_template('welcome.html',logging = 'Sorry,You have liked this blog.')
        text.likes += 1
        text.likesUser += session['username']
        re = t.commit()
    if int(a) == 4:
        if session['username'] in text.collectionUser:
            return render_template('welcome.html',logging = 'Sorry,You have collected this blog.')
        text.collection +=1
        text.collectionUser += session['username']
        re = t.commit()
    if re == 'yes':
        return redirect(url_for('welcome'))
    else:
        return render_template('welcome.html',logging = 'Sorry,operation failed!')

@app.route('/add_body')
def add_body():
    a = request.values.get('add_text')
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        t = Usertext()
        re = t.inset(session['username'],a,nowtime)
        if re != 'yes':
            return render_template('welcome.html',logging='Inset text faild.')
    except Exception,e:
        print e
        return redirect(url_for('welcome'))
    return redirect(url_for('welcome'))
#    if re == 'yes' and re_t == 'yes':

#    else:
#        return render_template('welcome.html',logging = 'Faile')

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
            u=User(username=request.form['username'],
                   password=request.form['password'],
                   email=request.form['email'],
                   phone=request.form['phone'],
                   )
            re_log= User.inset(u)
            if re_log == 'yes':
                return redirect(url_for('welcome.html'))
            else:
                pass


@app.route('/login',methods=['GET','POST'])
def login():
    try:
        if request.method == 'GET':
            if session['username']:
                return redirect(url_for('welcome'))
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
                    return redirect(url_for('welcome'))
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
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    #app.run()