from django.contrib import admin

from .models import User, Theme, Room, Message, BinaryRoom, Clip

# Register your models here.
admin.site.register(User)
admin.site.register(Theme)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Clip)
admin.site.register(BinaryRoom)
