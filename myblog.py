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
    left_func = LeftFunction()
    # try:
    dic_wel = left_func.welcome(session['username'])
    return render_template('welcome.html', name=session['username'], text_info=dic_wel['blog_body'], tweets=dic_wel['blog_count_num'],
                                    praise=dic_wel['praise_num'], forward=dic_wel['forward_num'], comment=dic_wel['comment_num'],
                                    likes=dic_wel['likes_num'], collection=dic_wel['collect_num'], care=dic_wel['care_num'],
                                   fans=dic_wel['fans_num'])
    # except Exception,e:
    #     print e.message
    #     print '用户未登录，返回主页。'
    #     dic_wel = left_func.not_login_welcome()
    #     return render_template('welcome.html', text_info=dic_wel['blog_body'], prompt=u'登录后显示', forward=dic_wel['forward_num'],
    #                            comment=dic_wel['comment_num'], likes=dic_wel['likes_num'], collection=dic_wel['collect_num'])


@app.route('/search')
def search():
    a = request.values.get('search_body')
    #sql = "SELECT * FROM Usertext WHERE find_in_set(a, text);"
    #print b
    return redirect(url_for('welcome'))

@app.route('/add_fclc')
def add_fclc():
    act_id = int(request.values.get('fclc'))
    text_id = request.values.get('textid')
    text_act = TextOperation()
    now_time = datetime.datetime.now()
    comment_body = request.values.get('body')
    try:
        act_re = text_act.choose_act_name(act_id, session['username'], now_time, text_id, comment_body)
        if act_re != 'yes':
            return render_template('welcome.html', logging = act_re)
        return redirect(url_for('welcome'))
    except Exception, e:
        return render_template('welcome.html', logging = u'请先登录.')


@app.route('/add_body')
def add_body():
    a = request.values.get('add_text')
    print a
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        user = session['username']
    except Exception, e:
        return render_template('welcome.html', logging = u'登录后才能发送博客。')
    try:
        t = Usertext()
        re = t.inset(user,a,nowtime)
        if re != 'yes':
            return render_template('welcome.html',logging=u'发送博客失败。')
    except Exception,e:
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
    left_func = LeftFunction()
    try:
        dic_collect_blog = left_func.collect(session['username'])
        return render_template('collect.html', name=session['username'], text_info=dic_collect_blog['blog_body'], tweets=dic_collect_blog['blog_count_num'],
                                praise=dic_collect_blog['praise_num'], forward=dic_collect_blog['forward_num'], comment=dic_collect_blog['comment_num'],
                                likes=dic_collect_blog['likes_num'], collection=dic_collect_blog['collect_num'],care=dic_collect_blog['care_num'],
                               fans=dic_collect_blog['fans_num'])
    except Exception, e:
        return render_template('welcome.html', logging = u'登录后显示收藏的内容。')


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
                return redirect(url_for('welcome'))
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