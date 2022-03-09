from django.contrib import admin
from account.models import *

class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name']

class DrugAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class ProfessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class CustomuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']

class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class DiagnosAdmin(admin.ModelAdmin):
    list_display = ['id','name']



admin.site.register(Customuser,CustomuserAdmin)
admin.site.register(Profession,ProfessionAdmin)
admin.site.register(Review)
admin.site.register(Diagnos,DiagnosAdmin)
admin.site.register(Disease,DiseaseAdmin)
admin.site.register(Drug,DrugAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Region,RegionAdmin)

