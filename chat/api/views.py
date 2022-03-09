from rest_framework import viewsets
from rest_framework import generics, mixins, views
from chat.models import *
from account.models import *
from chat.api.serializer import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import  mixins
from rest_framework import filters
from doctor.paginations import StandardResultsSetPagination 

class ThreadViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ThreadSerializer
    permission_classes = [AllowAny]
    queryset = Thread.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend,  filters.SearchFilter]
    filterset_fields = ['subject']
    search_fields = ['subject']

    def get_queryset(self):
        return Thread.objects.filter(particpaint__user=self.request.user).all()


class MessageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend,  filters.SearchFilter]
    filterset_fields = ['user']
    search_fields = ['user']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        particpaint = Particpaint.objects.filter(thread__slug=self.request.GET['slug'],user=self.request.user).first()
        if particpaint:
            particpaint.last_read = datetime.datetime.now()
            particpaint.save()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Message.objects.filter(thread__slug=self.request.GET['slug']).order_by("-created_at").all()


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def send_message(request):
    try:
        text = request.data.get('text')
        slug = request.data.get('thread')
        thread = Thread.objects.filter(slug=slug).first()
        if not thread:
            res = {
                'status': 0,
                'msg': 'Thread not found'
            }
            return Response(res)
        thread.send_message(text, request.user)
        res = {
            'status': 1,
            'msg': 'Sms send'
        }
        return Response(res)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)
