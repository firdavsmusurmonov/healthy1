from schedule.models import *
from rest_framework import viewsets
from .serializer import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def me_schedule(request):
    try:
        user = request.user
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



@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def reschedule_schedule(request):
    try:
        status = request.data.get('status')
        id = request.data.get('id')
        schedule = Schedule.objects.filter(id=id).first()
        if schedule:
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