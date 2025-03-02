from django.urls import path, re_path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.chats_list, name='chats_list'),
    re_path(r'^chat/(?P<chat_id>\d+)/$', views.messages_chat, name='messages_chat'),

    # login-section
    path('auth/login/', LoginView.as_view
         (template_name='login_page.html'), name='login_user'),
    path('auth/login/tg', views.login_by_tg_id, name='login_user_tg'),
    path('auth/logout/', views.logout_page, name='logout_user'),
]