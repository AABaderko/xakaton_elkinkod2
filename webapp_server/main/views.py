import json

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from django.contrib.auth import login, logout

from channels.generic.websocket import AsyncWebsocketConsumer

from .models import (
    AppUser, Chat, ChatMember, MessageChat
)

def login_by_tg_id(request):
    print(request.method)
    if request.method == 'POST':
        tg_id = request.POST.get('tg_id')
        print(request.POST)
        if tg_id:
            user = AppUser.objects.get(tg_id=tg_id)
            print(user)
            if not(user is None):
                login(request, user)
                return redirect('/')
    return redirect('login_user')

def logout_page(request):
    logout(request)
    return redirect('login_user')

def chats_list(request, *args, **kwargs):
    login_user = request.user
    if not login_user.is_authenticated:
        return redirect('login_user')
    context = {}

    chatmemb_list = ChatMember.objects.filter(user_id=login_user.id)
    context['chatmemb_list'] = chatmemb_list

    return render(request, "chat_list.html", context)

def messages_chat(request, chat_id, *args, **kwargs):
    login_user = request.user
    if not login_user.is_authenticated:
        return redirect('login_user')
    
    chat_member = ChatMember.objects.get(chat_id=chat_id, user_id=login_user)
    if not (chat_member):
        return redirect('chats_list')

    messages_list = MessageChat.objects.filter(chat_id = chat_id)
    if len(messages_list) > 0:
        messages_list.order_by('-sended_at')

    context = {
        'chat_id': chat_id,
        'user_id': login_user.id,
        'chat_member': chat_member,
        'messages_list': messages_list,
    }
    return render(request, "messages_chat.html", context)