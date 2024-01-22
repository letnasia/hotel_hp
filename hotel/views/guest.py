from drf_yasg.utils import swagger_auto_schema, no_body
from django.contrib.auth.models import User
from django.contrib import auth
from django.db import transaction
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, \
    authentication_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from hotel.exceptions import UserExists, InvalidCredentials
from hotel.models import Guest
from hotel.serializers.guest import GuestCreateSerializer, GuestSerializer, \
    GuestLoginSerializer


@swagger_auto_schema(
    methods=['post'],
    request_body=GuestCreateSerializer,
    responses={200: "OK"}
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def register(request):
    serializer = GuestCreateSerializer(data=request.data)

    if not serializer.is_valid():
        raise ValidationError()

    validated_data = serializer.validated_data

    with transaction.atomic():
        user = User.objects.filter(username=validated_data['login']).first()

        if user:
            raise UserExists()

        user = User.objects.create_user(
            username=validated_data['login'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.save()
        guest = Guest.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
        )
        auth.login(
            request,
            user,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        return Response(GuestSerializer(guest).data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=['post'],
    request_body=GuestLoginSerializer,
    responses={200: "OK"}
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    serializer = GuestLoginSerializer(data=request.data)

    if not serializer.is_valid():
        raise ValidationError()

    validated_data = serializer.validated_data
    user = auth.authenticate(
        request=request,
        username=validated_data['login'],
        password=validated_data['password'],
    )

    if user is None:
        raise InvalidCredentials()

    guest = Guest.objects.get(user=user)
    auth.login(request, user)
    return Response(GuestSerializer(guest).data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=['post'],
    request_body=no_body,
    responses={200: "OK"}
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    auth.logout(request)
    return Response({}, status=status.HTTP_200_OK)
