from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework.views import APIView
from django.db.models import Q

class registration(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_email(data)
            return Response({
                "message": "User created successfully", 
                 "status" : status.HTTP_201_CREATED
                })
        return Response({
            "message": "Invalid data",
            "error" : serializer.errors,
            "status" : status.HTTP_400_BAD_REQUEST
        })

class login(APIView):
    def post(self, request):
        data = dict(request.data)
        try:
            user = User.objects.get(email=data['email'][0])
        except User.DoesNotExist:
            return Response({
                "message": "User not found",
                "status" : status.HTTP_404_NOT_FOUND
                })
        if user.check_password(data['password'][0]):
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "status" : status.HTTP_200_OK
                })
        return Response({
            "message": "Invalid password",
            "status" : status.HTTP_401_UNAUTHORIZED
            })

class search(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.get(id = request.user.id)
        imei = int(request.data['IMEI'])
        instance_imei = device_detail.objects.filter(Q(imei1=imei) | Q(imei2=imei)).first()
        if instance_imei:
            serializer = deviceSerializer(instance_imei)
            if instance_imei.report_by != user:            
                search_instance = search_record.objects.create(search_device=instance_imei,search_user=user)
            return Response({
                "message": "Device found",
                "status" : status.HTTP_200_OK,
                "data" : serializer.data
                })
        else:
            return Response({
                "message": "Device not found",  
                "status" : status.HTTP_404_NOT_FOUND
                })
            
class userview(ModelViewSet): 
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['username','email','first_name','last_name']
    filter_backends=[filters.OrderingFilter,filters.SearchFilter]
    search_fields=['username','email','first_name','last_name']

    def get_queryset(self):
        user = self.request.user
        queryset=User.objects.filter(id = user.id)
        return queryset

    def get_serializer_class(self):
        if self.request.method in ['create','update','partial-update']:
            return UserSerializer
        return UserListSerilizer

    def list(self, request, *args, **kwargs):
        filter_query=self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(filter_query, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'list users successfully',
            'data': serializer.data,
        }) 
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'retrieve user successfully',
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'update user successfully',
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'delete user successfully',
        })
    
class deviceview(ModelViewSet): 
    queryset = device_detail.objects.all()
    serializer_class = deviceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['username','email','first_name','last_name']
    filter_backends=[filters.OrderingFilter,filters.SearchFilter]
    search_fields=['username','email','first_name','last_name']

    def get_queryset(self):
        user = self.request.user
        queryset = device_detail.objects.filter(report_by=user)
        return queryset
    
    def list(self, request, *args, **kwargs):
        filter_query=self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(filter_query, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'list all your missing report successfully',
            'data': serializer.data,
        }) 
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'add missing report successfully',
            })
        return Response({
            "message": "Invalid data",
            "error" : serializer.errors,
            "status" : status.HTTP_400_BAD_REQUEST
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance,context={'request': request})
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'retrieve missing report\'s detail successfully',
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        data = request.data
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=data, partial=partial,context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'update your missing report\'s details successfully',
        })
    
    def destroy(self, request, *args, **kwargs):
        data = request.user.id
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'delete your missing report successfully',
        })
    
class searchview(ModelViewSet): 
    serializer_class = SearchSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['search_device','search_date']
    filter_backends=[filters.OrderingFilter,filters.SearchFilter]
    search_fields=['search_device']

    def get_queryset(self,device=None):
        user = self.request.user
        queryset = search_record.objects.filter(search_device__report_by=user,search_device__id=device)
        return queryset

    def list(self, request, *args, **kwargs):
        device = self.request.query_params.get('device_id')
        filter_query=self.filter_queryset(self.get_queryset(device))
        serializer = self.serializer_class(filter_query, many=True,context={'request': request})
        
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'list all your missing report successfully',
            'data': serializer.data,
        }) 
        

from mobile_tracking.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
def send_email(data):
    subject = 'Welcome to FIND MISSING DEVICES'
    text_content = 'Welcome to FIND MISSING DEVICES - Your login credentials are enclosed below.'

    html_content = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Welcome to FIND MISSING DEVICES</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <table width="100%" style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <tr>
                <td style="background-color: #00695c; padding: 20px; color: white; border-top-left-radius: 10px; border-top-right-radius: 10px; text-align: center;">
                    <h2 style="margin: 0;">FIND MISSING DEVICES</h2>
                </td>
            </tr>
            <tr>
                <td style="padding: 20px;">
                    <p style="font-size: 16px; color: #333;"><strong>Dear {data['first_name']}  {data['last_name']},</strong></p>
                    <p style="font-size: 15px; color: #333;">Welcome to FIND MISSING DEVICES. Your account has been successfully created.</p>
                    
                    <p style="font-size: 15px; color: #333;">Below are your login credentials:</p>
                    <ul style="font-size: 15px; color: #333; padding-left: 20px;">
                        <li><strong>Username:</strong> {data['email']}</li>
                        <li><strong>Password:</strong> {data['password']}</li>
                    </ul>

                    <p style="font-size: 14px; color: #666;">Please use the credentials above to log into the FIND MISSING DEVICES portal. You are advised to change your password upon first login for security purposes.</p>
                    
                    <br/>
                    <p style="font-size: 14px; color: #999;">If you need any assistance, feel free to reach out to the FIND MISSING DEVICES help desk.</p>
                    <p style="font-size: 14px; color: #999;">Regards,<br/>FIND MISSING DEVICES Team</p>
                </td>
            </tr>
            <tr>
                <td style="background-color: #e0f2f1; padding: 15px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; text-align: center; font-size: 13px; color: #555;">
                    © 2025 Find Missing Devices. All Rights Reserved.
                </td>
            </tr>
        </table>
    </body>
    </html>"""

    from_email = EMAIL_HOST_USER
    to_emails = [data['email']]
    email = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    email.attach_alternative(html_content, 'text/html')
    email.send()