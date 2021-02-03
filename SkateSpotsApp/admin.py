from django.contrib import admin

# Register your models here.
from SkateSpotsApp.models import User, Message, Comment, Marker

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Marker)
