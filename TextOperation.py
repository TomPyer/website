# coding:utf-8
#!/usr/bin/python

from models.u_user import User
from models.t_usertext import Usertext
from models.t_actlog import t_actlog
from models.t_comment import CommentBody



class TextOperation(object):
    """
        对于博客文本的四种操作，暂定四种（点赞like，评论comment，转发forward，收藏collection）
    """

    def __init__(self):
        self.user_text_obj = Usertext()
        self.user_obj = User()
        self.act_log_obj = t_actlog()
        self.insert_comment = CommentBody()

    def like(self, user_code, date, blog_text_id ):
        text_obj = Usertext.query.filter_by(id=blog_text_id).first()
        if user_code in text_obj.likesUser:
            return False
        text_obj.likes += 1
        text_obj.likesUser += (',' + user_code)
        self.user_text_obj.commit()
        log_ret = t_actlog.inset(act_user=user_code, text_code=blog_text_id, act_time=date, act_name="like",)
        self.act_log_obj.commit()
        return log_ret

    def comment(self, user_code, comment_body, date, blog_text_id ):
        text_obj = Usertext.query.filter_by(id= blog_text_id).first()
        text_obj.comment +=1
        text_obj.commentUser += (',' + user_code)
        self.user_text_obj.commit()
        self.insert_comment.inset(user_code, blog_text_id, date, comment_body)
        log_ret = t_actlog.inset(act_user=user_code, text_code=blog_text_id, act_time=date, act_name="comment")
        self.act_log_obj.commit()
        return log_ret

    def forward(self, user_code, date, blog_text_id ):
        text_obj = Usertext.query.filter_by(id=blog_text_id).first()
        if user_code in text_obj.forwardUser:
            return False
        text_obj.forward += 1
        text_obj.forwardUser += (',' + user_code)
        self.user_text_obj.commit()
        log_ret = t_actlog.inset(act_user=user_code, text_code=blog_text_id, act_time=date, act_name="forward")
        self.act_log_obj.commit()
        return log_ret

    def collection(self, user_code, date, blog_text_id ):
        text_obj = Usertext.query.filter_by(id=blog_text_id).first()
        if user_code in text_obj.collectionUser:
            return False
        text_obj.collection += 1
        t_actlog.collectionUser += (',' + user_code)
        self.user_text_obj.commit()
        log_ret = t_actlog.inset(act_user=user_code, text_code=blog_text_id, act_time=date, act_name="forward")
        self.act_log_obj.commit()
        return log_ret


