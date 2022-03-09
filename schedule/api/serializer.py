from rest_framework import serializers
from schedule.models import *
from account.models import *
from account.api.serializer import DoctorSerializer,ProfessionSerializer


class DoctorUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customuser
        fields = ["fullname","avatar",'profession',]

class ScheduleSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['user','doctor','start_datetime','desc','status']

    def get_doctor(self, obj):
        return DoctorUserSerializer(obj.doctor, many=False, context={"request": self.context["request"]}).data

