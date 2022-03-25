from django.contrib import admin
from .models import *
from schedule.models import *


# Register your models here.

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status']


admin.site.register(Schedule, ScheduleAdmin)
