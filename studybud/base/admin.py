from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, User

# adds the room data into the admin page so we can visually see it 
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)