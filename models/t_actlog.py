# coding:utf-8
#!/usr/bin/python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import MySQLdb

app=Flask(__name__)
app.config['SECRET_KEY'] ='hard to guess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:wobuzhidaoA123.@localhost:3306/flask_work'
db = SQLAlchemy(app)

class t_actlog(db.Model):
    __tablename__ = 't_actlog'

    id = db.Column(db.Integer,primary_key=True)
    actUser = db.Column(db.String(80),index=True)
    textCode = db.Column(db.String(100),index=True)
    actTime = db.Column(db.DateTime,index=True)
    actName = db.Column(db.String(100), index=True)

    def __repr__(self):
        return '%s (%r,%r,%r)' %(self.__class__.__name__,self.user,self.text,self.createTime)

    def inset(self, act_user, text_code, act_time, act_name):
        a = t_actlog(actUser=act_user,textCode=text_code,actTime=act_time, actName= act_name)
        db.session.add(a)
        print '插入数据中'
        db.session.commit()
        return 'yes'

    def commit(self):
        db.session.commit()
        return 'yes'

    def add_comment(self,user,text,createtime):
        pass

    def into_sql(sql):
        db.engine.execute(sql)
        return 'yes'

if __name__ == "__main__":
    db.create_all()