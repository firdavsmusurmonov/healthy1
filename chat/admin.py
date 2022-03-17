from django.contrib import admin
from .models import *
# Register your models here.


class ThreadAdmin(admin.ModelAdmin):
    list_display = ['id','slug']
    search_fields = ['slug']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id','thread']
    search_fields = ['thread']

class ParticpaintAdmin(admin.ModelAdmin):
    list_display = ['id','user']
    search_fields = ['name']


admin.site.register(Thread,ThreadAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Particpaint,ParticpaintAdmin)