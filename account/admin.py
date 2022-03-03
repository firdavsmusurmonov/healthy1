from django.contrib import admin
from account.models import *

class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']

class DrugAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class CustomuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']

class DiagnosAdmin(admin.ModelAdmin):
    list_display = ['id','name']


admin.site.register(Customuser,CustomuserAdmin)
admin.site.register(Profession)
admin.site.register(Review)
admin.site.register(Diagnos,DiagnosAdmin)
admin.site.register(Disease)
admin.site.register(Drug,DrugAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Region,RegionAdmin)

