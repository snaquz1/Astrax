from django.contrib import admin

from Chat.models import *
from Users.models import CustomUser

# Register your models here.
admin.site.register(Chat)
admin.site.register(ChatMember)
admin.site.register(Message)