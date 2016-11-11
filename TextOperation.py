# coding:utf-8
#!/usr/bin/python

from models.u_user import User
from models.t_usertext import Usertext
from models.t_actlog import t_actlog
from models.t_comment import CommentBody
import copy



class TextOperation(object):
    """
        对于博客文本的四种操作，暂定四种（点赞like，评论comment，转发forward，收藏collection）
    """

    def __init__(self):
        self.user_text_obj = Usertext()
        self.user_obj = User()
        self.act_log_obj = t_actlog()
        self.insert_comment = CommentBody()
        self.act_log = ''

    def choose_act_name(self, act_num, user_code, date, blog_text_id, comment_body):
        text_obj = Usertext.query.filter_by(id=blog_text_id).first()
        if act_num == 1:
            self.forward(text_obj, user_code, date, blog_text_id)
        if act_num == 2:
            self.comment(text_obj, user_code, date, blog_text_id, comment_body)
        if act_num == 3:
            self.like(text_obj, user_code, date, blog_text_id)
        if act_num == 4:
            self.collection(text_obj, user_code, date, blog_text_id)
        return self.act_log

    def like(self, text_obj, user_code, date, blog_text_id ):
        if user_code in text_obj.likesUser:
            self.act_log = u'您已经为这条博客点赞过。'
        else:
            text_obj.likes += 1
            text_obj.likesUser += (',' + user_code)
            self.user_text_obj.commit()
            self.act_log = self.act_log_obj.inset(user_code, blog_text_id, date, "like",)
            self.act_log_obj.commit()

    def comment(self, text_obj, user_code, comment_body, date, blog_text_id):
        text_obj.comment +=1
        text_obj.commentUser += (',' + user_code)
        self.user_text_obj.commit()
        self.insert_comment.inset(user_code, blog_text_id, date, comment_body)
        self.act_log = self.act_log_obj.inset(user_code, blog_text_id, date, "comment")
        self.act_log_obj.commit()
        return self.act_log

    def forward(self, text_obj, user_code, date, blog_text_id ):
        if user_code in text_obj.forwardUser:
            self.act_log = u'您已经转发过这条博客。'
        elif text_obj.user == user_code:
            self.act_log = u'不能转发自己的博客。'
        else:
            #添加转发信息,转发数+1,添加转发人.
            text_obj.forward += 1
            text_obj.forwardUser += (',' + user_code)
            #复制原文本,使用转发人user_code发送新博客.
            text_body = text_obj.text
            self.user_text_obj.inset(user_code, text_body, date)
            self.user_text_obj.commit()
            self.act_log = self.act_log_obj.inset(user_code, blog_text_id, date, "forward")
            self.act_log_obj.commit()
        return self.act_log

    def collection(self, text_obj, user_code, date, blog_text_id):
        if user_code in text_obj.collectionUser:
            self.act_log = u'您已经收藏过这条博客。'
        else:
            text_obj.collection += 1
            text_obj.collectionUser += (',' + user_code)
            self.user_text_obj.commit()
            self.act_log = self.act_log_obj.inset(user_code, blog_text_id, date, "forward")
            self.act_log_obj.commit()
        return self.act_log


