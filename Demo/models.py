from django.db import models
from db.abstract_model import AbstractModel
# Create your models here.


class ChatInfo(AbstractModel):
    # 用户id
    user_id = models.CharField(max_length=50, default="用户id",verbose_name="用户ID")
    # 用户名
    user_name = models.CharField(max_length=50, default="匿名",verbose_name="用户名")
    # 用户IP
    user_ip = models.CharField(max_length=30, default="127.0.0.1", verbose_name="用户IP")
    # 用户发送的内容
    chat_content = models.CharField(max_length=400, default="空", verbose_name="发送的内容")

    class Meta:
        verbose_name = "聊天内容"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.chat_content

class UserInfo(AbstractModel):
    # 用户id
    user_id = models.CharField(max_length=50, default="用户id", verbose_name="用户ID")
    # 用户名
    user_name = models.CharField(max_length=50, default="匿名用户", verbose_name="用户名")
    # 用户所属ip
    user_ip = models.CharField(max_length=30, default="1.1.1.1", verbose_name="用户IP")

