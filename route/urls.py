from account.api.views import *
from schedule.api.views import *
from chat.api.views import ThreadViewSet, MessageViewSet, send_message
from account.api.views import RegionViewSet,update_profil_img
from schedule.api.views import set_status,reschedule_schedule,me_canceled
from rest_framework import routers, serializers, viewsets

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'threads', ThreadViewSet)
router.register(r'message', MessageViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'region1', RegionViewSet)
router.register(r'diagnos', DiagnosViewSet)
router.register(r'disease', DiseaseViewSet)
router.register(r'drug', DrugViewSet)
router.register(r'profession', ProfessionViewSet)
router.register(r'doctorchoose', DoctorViewSet)


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('register', register),
    path('send-gmail', send_gmail),
    path('get-result', get_result),
    path('register-accepted', register_accepted),
    path('login', login),
    path('profil', profil),
    path('set-password', set_password),
    path('forget-password', forget_password),
    path('forget-password-accepted', forget_password_accepted),
    path('forget-password-update', forget_password_update),
    path('me', me),
    path('doctor', doctor),
    path('region', region),
    path('doctor-detail', doctor_detail),
    path('me-schedule', me_schedule),
    path('create-schedule', create_schedule),
    path('send-message', send_message),
    path('set-status', set_status),
    path('me-canceled', me_canceled),
    path('reschedule-schedule', reschedule_schedule),
    path('update-profil-img', update_profil_img)
]
urlpatterns += router.urls
