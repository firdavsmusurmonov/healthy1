from rest_framework import serializers
from schedule.models import *
from account.api.serializer import DoctorSerializer,ProfessionSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customuser
        fields = ["fullname","avatar"]




class ScheduleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = "__all__"

    def get_user(self, obj):
        return UserSerializer(obj.user, many=False, context={"request": self.context["request"]}).data

    def get_profession(self, obj):
        return ProfessionSerializer(obj.doctor, many=False, context={"request": self.context["request"]}).data
