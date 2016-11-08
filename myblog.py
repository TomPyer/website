# coding:utf-8
#!/usr/bin/python

from flask import request
from flask import session, redirect, url_for, escape, flash
from flask import render_template
from flask import Flask
from models.u_user import User
from models.t_usertext import Usertext
from flask_sqlalchemy import SQLAlchemy
from TextOperation import TextOperation
from LeftFunction import LeftFunction
import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect(url_for('welcome'))

@app.route('/welcome',methods=['GET','POST'])
def welcome():
    '''print User.query.limit(10).all() #查询返回的数据的数目

        data_all=User.query.all()me
        print (data_all)#查询全部

        for i in range(len(data_all)):
         print data_all[i].username+" "+data_all[i].email+" "+data_all[i].phone
    '''

    left_func = LeftFunction()
    if session['username']:
        dic_wel = left_func.welcome(session['username'])
        return render_template('welcome.html', name=session['username'], text_info=dic_wel['blog_body'], tweets=dic_wel['blog_count_num'],
                                praise=dic_wel['praise'], forward=dic_wel['forward_num'], comment=dic_wel['comment_num'],
                                likes=dic_wel['likes_num'], collection=dic_wel['collect_num'])
    else:
        username = ''
        dic_wel = left_func.welcome(username)
        return render_template('welcome.html', text_info=dic_wel['blog_body'], prompt=u'登录后显示', forward=dic_wel['forward_num'],
                               comment=dic_wel['comment_num'], likes=dic_wel['likes_num'], collection=dic_wel['collect_num'])


@app.route('/search')
def search():
    a = request.values.get('search_body')
    #sql = "SELECT * FROM Usertext WHERE find_in_set(a, text);"
    #print b
    return redirect(url_for('welcome'))

@app.route('/add_fclc')
def add_fclc():
    a = request.values.get('fclc')
    b = request.values.get('textid')
    text_act = TextOperation()
    now_time = datetime.datetime.now()
    try:
        if int(a) == 1 :
            act_re = text_act.forward(session["username"], now_time, b,)
            if not act_re :
                return render_template('welcome.html', logging =u'您已经转发过这条博客。')
        elif int(a) == 2:
            comment_body = request.values.get('body')
            text_act.comment(session["username"], now_time, b, comment_body)
        elif int(a) == 3:
            act_re = text_act.like(session["username"],now_time, b)
            if not act_re:
                return render_template('welcome.html', logging =u'您已经为这条博客点赞过。')
        elif int(a) == 4:
            act_re = text_act.collection(session['username'], now_time, b)
            if not act_re:
                return render_template('welcome.html', logging =u'您已经收藏过这条博客。')

        return render_template('welcome.html')

    except Exception, e:
        return render_template('welcome.html', logging = u'请先登录.')


@app.route('/add_body')
def add_body():
    a = request.values.get('add_text')
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = session['username']
    try:
        t = Usertext()
        re = t.inset(user,a,nowtime)
        if re != 'yes':
            return render_template('welcome.html',logging=u'查询信息失败。')
    except Exception,e:
        print e.message
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
    forward_num = int(0)
    comment_num = int(0)
    likes_num = int(0)
    collect_num = int(0)
    try:
        b = Usertext.query.filter_by(user=session['username']).all()
        c = Usertext.query.filter_by(user=session['username']).count()
        praise_num = 0

        for i in b :
            praise_num += i.likes

        for u in b :
            forward_num += u.forward
            comment_num += u.comment
            likes_num += u.likes
            collect_num += u.collection

        b = b[::-1]
    except Exception, e:
        pass

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
            return render_template('register.html',logging=u'用户名已被注册。')
        elif b > 0:
            return render_template('register.html',logging=u'邮箱已被注册。')
        elif c >0:
            return render_template('register.html',logging=u'手机号已被注册。')
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
            a = {'username':'','password':'','email':'','phone':'',}
            try:
                u = User.query.filter_by(username = request.form['username']).first()
                if u.password == request.form['password']:
                    session['username']= request.form['username']
                    return redirect(url_for('welcome'))
            except Exception,e:
                print 'fail %s'%e
            return render_template('login.html',logging=u'用户名或密码错误！')
        else:
            return render_template('login.html',logging=u'用户名或密码不能为空！')

@app.route('/logout',methods=['GET','POST'])
def logout():
    if request.method == 'GET':
        session.pop('username',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
        pass

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    #app.run()