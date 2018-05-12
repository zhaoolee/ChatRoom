import xadmin

from .models import *
# Register your models here.

class ChatInfoAdmin(object):
    # 定义需要显示的大主题
    list_display = ['user_name', 'user_ip', 'chat_content']



xadmin.site.register(ChatInfo, ChatInfoAdmin)
