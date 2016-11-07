# coding:utf-8
#!/usr/bin/python

from flask import request
from flask import session, redirect, url_for, escape, flash
from flask import render_template
from flask import Flask
from models.u_user import User
from models.t_usertext import Usertext
from models.t_actlog import t_actlog
from flask_sqlalchemy import SQLAlchemy
import datetime


class TextOperation(object):
    """
        对于博客文本的四种操作，暂定四种（点赞like，评论comment，转发forward，收藏collection）
    """

    def __init__(self):
        self.user_text_obj = Usertext()
        self.user_obj = User()
        self.act_log_obj = t_actlog()

    def like(self, user_code, date, blog_text_id ):
        text_obj = Usertext.query.filter_by(id=blog_text_id).first()
        if user_code in text_obj.likesUser:
            return False
        text_obj.likes += 1
        text_obj.likesUser += user_code
        self.user_text_obj.commit()
        log_ret = t_actlog.inset(act_user=user_code, text_code=blog_text_id, act_time=date, act_name="like",)
        self.act_log_obj.commit()


    def comment(self, user_code, comment_body, date, blog_text_id ):
        pass

    def forward(self, user_code, blog_text_user_code, date, blog_text_id ):
        pass

    def collection(self, user_code, date, blog_text_id ):
        pass


