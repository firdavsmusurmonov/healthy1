from rest_framework import serializers
from account.models import *
from django.db.models import Avg


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["id","name"]


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields =["id","name"]

class ProfileSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    class Meta:
        model = Customuser
        fields = ["id","fullname","avatar","username","email","gender","phone","birth_date","region","city"]
    
    def get_region(self, obj):
        return RegionSerializer(obj.region, many=False, context={'request': self.context['request']}).data
    
    
    def get_city(self, obj):
        return RegionSerializer(obj.city, many=False, context={'request': self.context['request']}).data

class CustomuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["id","username","phone","smscode"]

class CustomuserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["id","username"]

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["id","password","username"]

class SetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["id","password","phone"]

class ForgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["id","username","smscode"]

class ForgetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["id","username","password"]

class DoctorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields ="__all__"

class ChooseDoctorSerializer(serializers.ModelSerializer):
    review_avg = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

    class Meta:
        model = Customuser
        fields = ["id","fullname","avatar","review_avg","review_count","profession","region","city"]

    def get_review_avg(self, obj):
        return Review.objects.filter(doctor=obj).aggregate(avg_rating=Avg('start'))['avg_rating']

    def get_review_count(self, obj):
        return Review.objects.filter(doctor=obj).count()

    def get_profession(self, obj):
        return ProfessionSerializer(obj.profession, many=False, context={"request": self.context["request"]}).data

    def get_region(self, obj):
        return RegionSerializer(obj.region, many=False, context={'request': self.context['request']}).data

    def get_city(self, obj):
        return RegionSerializer(obj.city, many=False, context={'request': self.context['request']}).data


class DoctorSerializer(serializers.ModelSerializer):
    review_avg = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

    class Meta:
        model = Customuser
        fields = ["id","fullname","avatar","gender","bio","langtude","latitude","review_avg","review_count","profession","region","city"]

    def get_review_avg(self, obj):
        return Review.objects.filter(doctor=obj).aggregate(avg_rating=Avg('start'))['avg_rating']

    def get_review_count(self, obj):
        return Review.objects.filter(doctor=obj).count()

    def get_profession(self, obj):
        return ProfessionSerializer(obj.profession, many=False, context={"request": self.context["request"]}).data

    def get_region(self, obj):
        return RegionSerializer(obj.region, many=False, context={'request': self.context['request']}).data

    def get_city(self, obj):
        return RegionSerializer(obj.city, many=False, context={'request': self.context['request']}).data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class DiagnosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnos
        fields =["id","name","text"]

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = "__all__"

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = "__all__"

class DiseaseDetailSerializer(serializers.ModelSerializer):
    durgs = serializers.SerializerMethodField()
    class Meta:
        model = Disease
        fields = "__all__"

    def get_durgs(self, obj):
        return DrugSerializer(obj.drugs,many=True, context={"request": self.context["request"]}).data