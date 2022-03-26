from django.contrib import admin
from account.models import *


class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    search_fields = ['name']


class DrugAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

class VersionAdmin(admin.ModelAdmin):
    list_display = ['id', 'version']
    search_fields = ['version_name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ProfessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class CustomuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_doctor']
    list_editable = ['is_doctor']
    # list_filter = ['is_doctor', 'gender']
    # search_fields = ['username']


class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    filter_horizontal = ['drugs']


class DiagnosAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    filter_horizontal = ['disease', 'drugs']


admin.site.register(Customuser, CustomuserAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Review)
admin.site.register(Diagnos, DiagnosAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Version, VersionAdmin)
