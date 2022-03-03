from account.models import *
from rest_framework import viewsets
from .serializer import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import random
from rest_framework import status, generics, filters
from rest_framework_jwt.settings import api_settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import  mixins
from rest_framework import filters
from doctor.paginations import StandardResultsSetPagination 
from rest_framework.pagination import LimitOffsetPagination

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Customuser.objects.all()
    serializer_class = CustomuserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,  filters.SearchFilter]
    filterset_fields = ['first_name']
    search_fields = ['first_name']

class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,  filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

class ProfessionViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,  filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

class RegionViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Region.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend,  filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

class DiagnosViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    serializer_class = DiagnosSerializer
    permission_classes = [IsAuthenticated]
    queryset = Diagnos.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend,  filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

class DrugViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    serializer_class = DrugSerializer
    permission_classes = [IsAuthenticated]
    queryset = Drug.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend,  filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

class DiseaseViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Disease.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend,  filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            serializer_class = DiseaseSerializer           
        else:
            serializer_class = DiseaseDetailSerializer

        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def region(request):
    region_id = request.GET.get("region_id")
    if region_id:
        region = Region.objects.filter(parent_id=region_id).all()    
    else:
        region = Region.objects.filter(parent__isnull=True).all()
    
    res = {
        'status': 1,
        'data': RegionSerializer(region, many=True, context={"request":request}).data,
    }
    return Response(res)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    try:
        username = request.data.get('username')
        phone = request.data.get('phone')
        password = request.data.get('password')
        smscode = request.data.get('sms_code')
        if not username:
            res = {
                'msg': 'Login empty',
                'status': 0,
            }
            return Response(res)

        user = Customuser.objects.filter(username=username).first()
        if not user:
            user = Customuser.objects.create(
                username=username,
                complete=0
            )
        elif user:
            res = {
                'msg': 'User exits',
                'status': 2,
            }
            return Response(res)

        smscode = random.randint(1000, 9999)
        user.set_password(str(password))
        user.phone=int(phone)
        user.smscode = smscode
        user.save()
        send_sms(phone, "Tasdiqlash codi "+ str(smscode))
        if user:
            result = {
                'status': 1,
                'msg': 'Sms sended',
                'user': CustomuserSerializer(user, many=False, context={"request": request}).data,
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            res = {
                'status': 0,
                'msg': 'Can not authenticate with the given credentials or the account has been deactivated'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)

@api_view(['POST'])
@permission_classes([AllowAny,])
def register_accepted(request):
    try:
        username = request.data.get('username')
        sms_code = request.data.get('sms_code')
        user = Customuser.objects.filter(username=username).first()
        
        if user and int(user.smscode) == int(sms_code):
            user.complete = 0
            user.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            result = {
                'status': 1,
                'msg': 'Sms sended',
                'user': ForgetSerializer(user, many=False, context={"request": request}).data,
                'token': token
            }
            
            return Response(result, status=status.HTTP_200_OK)  
        else:
            result = {
                'status': 1,
                'msg': 'Sms send not equal',
            }
            return Response(result, status=status.HTTP_200_OK)  
 
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        if not login:
            res = {
                'msg': 'Login empty',
                'status': 0,
            }
            return Response(res)

        user = Customuser.objects.filter(username=username).first()
        if not user:
            res = {
                'msg': 'Login or password wrond',
                'status': 0,
            }
            return Response(res)
        if user and user.complete == 0:
            res = {
                'msg': 'Sms not verifcations',
                'status': 0,
            }
        if user and user.check_password(password):
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            result = {
                'status': 1,
                'msg': 'Sms sended',
                'user': LoginSerializer(user, many=False, context={"request": request}).data,
                'token': token
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            res = {
                'status': 0,
                'msg': 'Can not authenticate with the given credentials or the account has been deactivated'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)

@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def update_profil_img(request):
    user = request.user 
    status = request.status   
    if 'avatar' in request.data:
        user.avatar = request.data['avatar']
        user.save()
    return  Response(status=status.HTTP_200_OK, data={'status': 'ok'})    

@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def profil(request):
    try:
        phone = request.data.get('phone')
        fullname = request.data.get('fullname')
        username = request.data.get('username')
        email = request.data.get('email')
        gender = request.data.get('gender')
        birth_date = request.data.get('birth_date')
        region = request.data.get('region')
        city = request.data.get('city')
        user = request.user
        user.phone = phone
        user.fullname = fullname
        user.username = username
        user.email = email
        user.gender = gender
        user.birth_date = birth_date
        user.region_id = region
        user.city_id = city
        if 'avatar' in request.data:
            user.avatar = request.data['avatar']
        user.save()

        result = {
            'status': 1,
            'msg': 'User updated',
            'user': ProfileSerializer(user, many=False, context={"request": request}).data

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
def me(request):
    try:
        user = request.user
        result = {
            'status': 1,
            'user': ProfileSerializer(user, many=False, context={"request": request}).data
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
def doctor_detail(request):
    try:
        user = Customuser.objects.filter(id=request.GET.get("doctor_id",0)).first()
        if user:
            result = {
                'status': 1,
                'user': DoctorSerializer(user, many=False, context={"request": request}).data
            }
        else:
            result = {
                'status': 1,
                'msg': "User not fount"
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
def set_password(request):
    try:
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            result = {
                'status': 1,
                'msg': 'User password updated',
                'user': SetPasswordSerializer(user, many=False, context={"request": request}).data,
                'token': token
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {
                'status': 1,
                'msg': 'User old password wrong'
            }
            return Response(result, status=status.HTTP_200_OK)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def forget_password(request):
    try:
        username = request.data.get('username')
        user = Customuser.objects.filter(username=username).first()
        if user:
            smscode = random.randint(1000, 9999)
            user.smscode = smscode
            user.save()
            send_sms(user.phone, "Tasdiqlash codi "+ str(smscode))       
            result = {
                'status': 1,
                'msg': 'Sms send',
                "phone":user.phone
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {
                'status': 1,
                'msg': 'User not found'
            }
            return Response(result, status=status.HTTP_200_OK)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def forget_password_accepted(request):
    try:
        username = request.data.get('username')
        sms_code = request.data.get('sms_code')
        user = Customuser.objects.filter(username=username).first()
        if user and int(user.smscode) == int(sms_code):
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            result = {
                'status': 1,
                'msg': 'Sms sended',
                'user': ForgetSerializer(user, many=False, context={"request": request}).data,
                'token': token
            }
            
            return Response(result, status=status.HTTP_200_OK)  
        else:
            result = {
                'status': 1,
                'msg': 'Sms send not equal',
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
def forget_password_update(request):
    try:
        new_password = request.data.get('new_password')
        user = request.user
        user.set_password(new_password)
        user.save()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        result = {
                'status': 1,
                'msg': 'User password updated',
                'user': ForgetUpdateSerializer(user, many=False, context={"request": request}).data,
                'token': token
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
def doctor(request):
    try:
        qs = Customuser.objects.filter(is_doctor=True)
        category_slug = request.GET.get("category_slug", '')
        if category_slug != '':
            qs = qs.filter(profession__category__slug=category_slug)
        doctors = qs.all()

        result = {
            'status': 1,
            'user': DoctorSerializer(doctors, many=True, context={"request": request}).data
        }
        return Response(result, status=status.HTTP_200_OK)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)

import requests
def send_sms(phone, message):
    
    print("SALOM")
    url = "https://notify.eskiz.uz/api/message/sms/send"

    payload={
        'mobile_phone': phone,
        'message':message,
        'from': '4546'
    }
    files=[

    ]
    headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvbm90aWZ5LmVza2l6LnV6XC9hcGlcL2F1dGhcL2xvZ2luIiwiaWF0IjoxNjQ0MjI2Njg0LCJleHAiOjE2NDY4MTg2ODQsIm5iZiI6MTY0NDIyNjY4NCwianRpIjoiTWtiMEdEeTd6UjFrdm5IcSIsInN1YiI6NSwicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.nAHeGgQOCu107fejDZA23HxHPD6cMXS2fFrDHBZ1620'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)