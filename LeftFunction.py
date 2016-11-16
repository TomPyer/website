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
import json

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
        self.user_text_obj = Usertext()
        self.user_info_obj = User()
        self.act_log = ''

    def get_fans_info(self, user_code):
        """
        获取用户粉丝信息,数量
        """
        user_info = self.user_info_obj.query.filter_by(username=user_code).first()
        self.dic_wel_info['fans_info'] = (user_info.fans.split(','))
        return len(user_info.fans.split(','))

    def get_care_info(self, user_code):
        """
        获取用户关注对象,数量
        """
        user_info = self.user_info_obj.query.filter_by(username=user_code).first()
        self.dic_wel_info['care_info'] = (user_info.careuser.split(','))
        return len(user_info.careuser.split(','))

    def get_praise_num(self, user_code):
        """
        获取用户被赞次数
        """
        praise_num = 0
        blog_body = self.user_text_obj.query.filter_by(user=user_code).all()
        for i in blog_body:
            praise_num += i.likes
        return praise_num

    def get_blog_fclc_info(self, blog_body):
        """
        获取用户博客被操作具体数量
        fclc:
            forward, collection, like, care
        """
        for i in blog_body:
            self.dic_wel_info['forward_num'] += i.forward
            self.dic_wel_info['comment_num'] += i.comment
            self.dic_wel_info['likes_num'] += i.likes
            self.dic_wel_info['collect_num'] += i.collection

    def get_user_fcpb_info(self, user_code):
        """
        获取用户的基本信息：
            fcpb:
                fans, care, praise, blog_count
        """
        user_fcpb_info = {}
        user_fcpb_info['fans_num'] = self.get_fans_info(user_code)
        user_fcpb_info['care_num'] = self.get_care_info(user_code)
        user_fcpb_info['praise_num'] = self.get_praise_num(user_code)
        user_fcpb_info['blog_count_num'] = self.user_text_obj.query.filter_by(user=user_code).count()
        return user_fcpb_info

    def get_user_blog_count(self, user_code):
        """
        获取用户所有的博客
        """
        blog_body = self.user_text_obj.query.filter_by(user=user_code).all()
        self.dic_wel_info['blog_body'] = blog_body[::-1]
        return blog_body

    def welcome(self, user_code):
        """
        用户登录后显示主页面
        """
        blog_body = self.get_user_blog_count(user_code)
        self.dic_wel_info['user_info'] = self.get_user_fcpb_info(user_code)
        self.get_blog_fclc_info(blog_body)
        return self.dic_wel_info

    def not_login_welcome(self):
        """
        用户未登录显示主页面,不含用户信息查询
        """
        blog_body = self.user_text_obj.query.all()
        self.get_blog_fclc_info(blog_body)
        self.dic_wel_info['blog_body'] = blog_body[::-1]
        return self.dic_wel_info

    def collect(self, user_code):
        """
        用户登录后显示收藏博客信息
        """
        collect_body = []
        blog_body = self.user_text_obj.query.all()
        for i in blog_body:
            all_collect_user = i.collectionUser.split(',')
            if user_code in all_collect_user:
                collect_body.append(i)
        self.get_blog_fclc_info(collect_body)
        self.dic_wel_info['user_info'] = self.get_user_fcpb_info(user_code)
        self.dic_wel_info['blog_body'] = collect_body[::-1]
        return self.dic_wel_info

    def message(self):
        """
        用户未查看到消息提醒
        """
        pass

    def community(self):
        """
        社区动态,规划中
        """
        pass

    def care(self, user_code):
        """
        用户登录后显示已关注人信息缩略面板
        需要返回的参数 dic_care_info,  type= dict
        dic[tweets] = blog_count_num
        dic[praise] = praise_count_num
        dic[care] = care_count_num
        dic[fans] = fans_count_num
        *dic[care_user_info] = 登录用户关注的对象信息 type=list
            care_user_info: username, tweets, fans, care, praise
        """
        self.dic_wel_info['login_user_info'] = self.get_user_fcpb_info(user_code)
        self.dic_wel_info['care_user_info'] = []
        self.get_care_info(user_code)
        for i in self.dic_wel_info['care_info']:
            self.dic_wel_info['care_user_info'].append(self.user_info_obj.query.filter_by(username=i).first())
        return self.dic_wel_info


