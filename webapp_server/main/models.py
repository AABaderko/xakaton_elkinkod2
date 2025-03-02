import zoneinfo
from django.db import models
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from timezone_field import TimeZoneField

from django.utils.translation import gettext_lazy as _

from .modules import randomstring

class AppUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_tg_user(self, tg_id, first_name, **extra_fields):
        if not tg_id:
            raise ValueError('Users must have an telegram id')
        if not first_name:
            raise ValueError('Users must have an first name')
        
        user = self.model(tg_id, first_name, **extra_fields)

        user.username = randomstring(20)
        gen_password = randomstring(20)

        user.set_password(gen_password)
        user.save
        return user


    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username=username, password=password, **extra_fields)

class AppUser(AbstractUser):
    id = models.AutoField(primary_key=True)

    tg_id = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True, default=randomstring(20))

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, default="", blank=True)

    timezone = TimeZoneField(choices_display="WITH_GMT_OFFSET", default="Asia/Novokuznetsk")

    workgroup = models.CharField(choices={
        "C": "Заказчик",
        "E": "Исполнитель",
        "A": "Администратор",
    }, default="C", max_length=1)

    objects = AppUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password", "first_name"]

    def set_password(self, password=None):
        if not password:
            password = randomstring(20)
        self.password = make_password(password)

    def get_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(AppUser, through="ChatMember")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('messages_chat', kwargs={'chat_id': self.pk})

class ChatMember(models.Model):
    user_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True)
    
    user_set_work_time_start = models.TimeField(blank=True, null=True)
    user_set_work_time_end = models.TimeField(blank=True, null=True)
    
    work_time_start = models.TimeField(blank=True, null=True)
    work_time_end = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.chat_id.name}: {self.user_id.first_name}"

class MessageChat(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='user_identificator')

    text = models.CharField(max_length=1000)
    original_text = models.CharField(max_length=1000, blank=True, null=True)

    sended_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(blank=True, null=True)

    deleted = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)

    readed_by = models.ManyToManyField(AppUser, related_name='readed_by')

    class Meta:
        ordering = ['sended_at']

    def __str__(self):
        return f"{self.chat_id.name}: {self.user_id.first_name} {self.sended_at}"