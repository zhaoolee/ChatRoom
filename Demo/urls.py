from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^happy/$', views.happy, name="happy"),
    url(r'^save_chat_log/$', views.save_chat_log, name="save_chat_log"),
    url(r'^get_near_log/$', views.get_near_log, name="get_near_log"),

]