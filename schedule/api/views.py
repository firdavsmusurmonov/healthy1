from doctor.settings import DATETIME_FORMAT
from schedule.models import *
from rest_framework import viewsets
from .serializer import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.shortcuts import render
from account.models import Customuser
from django.shortcuts import render
import datetime

# Create your views here.
def my_scheduled_job():
    Schedule.objects.filter(status="upcoming", start_datetime__lte=datetime.now()).update(status="completed")



@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def me_schedule(request):
    try:
        user = request.user
        status = request.GET['status']
        if status:
            schedule = Schedule.objects.filter(status=status).all()
            result = {
                'status': 1,
                'schedule': ScheduleSerializer(schedule, many=True, context={"request": request}).data
            }
            return Response(result)
        schedule = Schedule.objects.filter(user=user).order_by("-created_at").all()
        result = {
            'status': 1,
            'schedule': ScheduleSerializer(schedule, many=True, context={"request": request}).data
        }
        return Response(result, status=status.HTTP_200_OK)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def create_schedule(request):
    try:
        user = request.user
        schedule = Schedule.objects.create(
            user=request.user,
            status=request.data.get('status'),
            desc=request.data.get('desc'),
            start_datetime=request.data.get('start_datetime'),
            doctor_id=request.data.get('doctor')
        )
        schedule.save()
        result = {
            'status': 1,
            'schedule': ScheduleSerializer(schedule, many=False, context={"request": request}).data
        }
        return Response(result, status=status.HTTP_200_OK)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def me_canceled(request):
    try:
        status = request.GET['status']
        if status:
            schedule = Schedule.objects.filter(status=status).all()
            result = {
                'status': 1,
                'schedule': ScheduleSerializer(schedule, many=True, context={"request": request}).data
            }
            return Response(result)
        result = {
            'status': "Canceled not define",
        }
        return Response(result)

    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def set_status(request):
    try:
        id = request.data.get('id')
        status = request.data.get('status')
        schedule = Schedule.objects.filter(id=request.data.get('id')).first()
        if schedule:
            schedule.id = id
            schedule.status = status
            schedule.save()
        result = {
            'status': 1,
            'schedule': ScheduleSerializer(schedule, many=False, context={"request": request}).data
        }
        return Response(result)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }

    return Response(res)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def reschedule_schedule(request):
    try:
        user = request.user
        status = request.data.get('status')
        desc = request.data.get('desc')
        start_datetime = request.data.get('start_datetime')
        doctor_id = request.data.get('doctor')
        profession_id = request.data.get('profession')
        schedule = Schedule.objects.filter(id=request.data.get('id')).first()
        if schedule:
            schedule.status = status
            schedule.desc = desc
            schedule.doctor_id = doctor_id
            schedule.profession_id = profession_id
            schedule.start_datetime = start_datetime
            schedule.save()
        result = {
            'status': 1,
            'msg': 'Schedule updated',
            'schedule': ScheduleSerializer(schedule, many=False, context={"request": request}).data
        }
        return Response(result)

    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)
