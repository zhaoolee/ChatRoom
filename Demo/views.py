from django.shortcuts import render
from utils import wrappers
from .models import ChatInfo, UserInfo
from django.http import JsonResponse
import json
from django.db.models import Max
import time
# Create your views here.

# 返回基础页面
def happy(request):

    user_info = UserInfo()
    # 初始用户名为匿名用户

    user_name = "匿名用户"
    user_info.user_name = user_name
    # 利用时间产生临时ID
    user_id = int(time.time())
    user_info.user_id = user_id
    # 获取用户ip
    user_ip = wrappers.get_client_ip(request)
    user_info.user_ip = user_ip
    user_info.save()

    return render(request, 'chatroom/happy.html', locals())

# 保存聊天内容
def save_chat_log(request):
    try:
        print("后端收到了ajax消息")
        chatinfo = ChatInfo()

        # 获取前端传过来的数据
        chat_content = wrappers.post(request, "chat_content")
        user_ip = wrappers.get_client_ip(request)
        user_name = wrappers.post(request, "user_name")
        user_id = wrappers.post(request, "user_id")

        # 将数据存入数据库
        chatinfo.chat_content = chat_content
        chatinfo.user_ip = user_ip
        chatinfo.user_name = user_name
        chatinfo.user_id = user_id

        chatinfo.save()

        return JsonResponse({"ret":0})
    except:
        return JsonResponse({"ret":"保存出现问题"})
        pass


# 获取最近的聊天信息

def get_near_log(request):
    try:
        # 获取数据库内所有的信息
        all_info = ChatInfo.objects.all()

        # 获取数据库内最后一条消息的id
        id_max =ChatInfo.objects.aggregate(Max('id'))
        last_id = id_max["id__max"]
        # print("后台数据库内最新的id为", last_id)

        # 获取请求的id值
        old_last_id = wrappers.post(request, "last_id")
        print(old_last_id,"<-<-")
        print(old_last_id, type(old_last_id),"-->")
        # print("后台发送过来的id为",old_last_id)

        # 返回的信息字典,返回当前时间(current_date),返回信息列表(id_info)

        # 如果第一次请求,则回复最后一条消息的id
        if int(old_last_id) == 0:
            user_ip = wrappers.get_client_ip(request)
            result_dict = dict()
            result_dict["last_id"] = last_id
            result_dict["info"] = [{"id":"-->", "mess":"欢迎"+user_ip+"来到聊天室!", "user_name":"系统消息:"}]
            result_dict["user_id"] = ""
            result_dict = json.dumps(result_dict,ensure_ascii=False)
            # print("第一次握手")
            return JsonResponse({"data":result_dict})

        # 如果数据内没有消息更新
        elif int(old_last_id) >= int(last_id):
            result_dict = dict()
            result_dict["last_id"] = last_id
            result_dict["info"] = [{last_id:"欢迎再次来到聊天室!"}]
            result_dict["user_id"] = ""
            result_dict = json.dumps(result_dict,ensure_ascii=False)
            # print("一次无更新的交互")
            return JsonResponse({"data":result_dict})

        # 如果有消息更新
        else:
            # print("有更新的回复")
            result_dict = dict()
            # 获取新的消息对象集合
            the_new_info =ChatInfo.objects.filter(id__gt=old_last_id)
            # 创建消息列表
            mess_list = list()
            # 将最新的消息组成字典进行返回
            for info in the_new_info:
                # print(info)
                # print ("-->",info.chat_content, info.id)
                # 创建消息字典
                mess_dic = dict()
                mess_dic["id"] = info.id
                mess_dic["mess"] = info.chat_content
                # 将消息所属的用户添加到消息列表
                mess_dic["user_name"] = info.user_name
                mess_dic["user_id"] = info.user_id
                # 将消息字典添加到消息列表
                mess_list.append(mess_dic)


        result_dict["last_id"] = last_id
        result_dict["info"] = mess_list
        # result_dict["info"] = [{"id":3, "mess":"hahah"}, {"id":4, "mess":"666"}]
        result_dict = json.dumps(result_dict,ensure_ascii=False)
        # print("--->>>", type(result_dict))

        return JsonResponse({"data":result_dict})
    except:
        return JsonResponse({"ret":"刷新出现问题"})
        pass

