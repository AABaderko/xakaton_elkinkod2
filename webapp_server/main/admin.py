from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    AppUser, Chat, ChatMember, MessageChat
)
from .forms import UserCreationForm

@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'tg_id', 'username')
    add_form = UserCreationForm
    fieldsets = (
        ('Login info', {'fields': ('username', 'password', 'tg_id')}),
        ('User info', {'fields': ('first_name', 'last_name')}),
        (None, {'fields': ('timezone', 'workgroup')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'tg_id', 'first_name', 'last_name', 'timezone', 'workgroup', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)

@admin.register(ChatMember)
class ChatMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'user_id')
    ordering = ('id',)

@admin.register(MessageChat)
class MessageChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'user_id', 'sended_at', 'text', 'edited', 'deleted')
    ordering = ('id',)