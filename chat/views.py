from django.shortcuts import render
from account.models import Customuser
# Create your views here.
def my_scheduled_job():
  user = Customuser.objects.filter(id=4).first()
  user.fullname = "sasa"
  user.save()
