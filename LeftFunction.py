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
import datetime


class LeftFunction(object):
    def __init__(self):
        self.dic_wel_info = {}
        self.dic_wel_info['forward_num'] = 0
        self.dic_wel_info['comment_num'] = 0
        self.dic_wel_info['likes_num'] = 0
        self.dic_wel_info['collect_num'] = 0
        self.dic_wel_info['blog_count_num'] = 0
        self.dic_wel_info['blog_body'] = ''
        self.dic_wel_info['praise_num'] = 0
        self.user_text_obj = Usertext

    def welcome(self, user_code ):
        if user_code == '':
            blog_body = self.user_text_obj.query.all()
        else: blog_body = self.user_text_obj.query.filter_by(user=user_code).all()
        self.dic_wel_info['blog_count_num'] = self.user_text_obj.query.filter_by(user=user_code).count()
        for i in blog_body:
            self.dic_wel_info['praise_num'] += i.likes
        for u in blog_body:
            self.dic_wel_info['forward_num'] += u.forward
            self.dic_wel_info['comment_num'] += u.comment
            self.dic_wel_info['likes_num'] += u.likes
            self.dic_wel_info['collect_num'] += u.collect
        self.dic_wel_info['blog_body'] = blog_body[::-1]
        return self.dic_wel_info

    def collect(self):
        pass

    def message(self):
        pass

    def community(self):
        pass

    def care(self):
        pass

