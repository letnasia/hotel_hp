from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, \
    authentication_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from hotel.authenticators import ManagerKeyAuthenticator
from hotel.exceptions import RestaurantNotFound
from hotel.models import Restaurant
from hotel.serializers.restaurant import RestaurantSerializer, \
    RestaurantMenuItemsSerializer, RestaurantWithMenuSerializer


class RestaurantViewSet(ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
        ManagerKeyAuthenticator,
    )
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Restaurant.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RestaurantWithMenuSerializer
        else:
            return RestaurantSerializer


@swagger_auto_schema(
    methods=['post'],
    request_body=RestaurantMenuItemsSerializer,
    responses={200: "OK"}
)
@api_view(['POST'])
@authentication_classes([
    SessionAuthentication,
    TokenAuthentication,
    ManagerKeyAuthenticator
])
@permission_classes([IsAuthenticated, IsAdminUser])
def restaurant_menu_add(request):
    serializer = RestaurantMenuItemsSerializer(data=request.data)

    if not serializer.is_valid():
        raise ValidationError()

    validated_data = serializer.validated_data
    restaurant = Restaurant.objects.filter(id=validated_data['id']).first()

    if restaurant is None:
        raise RestaurantNotFound()

    restaurant.menu.add(*validated_data['items'])
    return Response({
        "id": validated_data['id'],
        "items": validated_data['items']
    }, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    methods=['post'],
    request_body=RestaurantMenuItemsSerializer,
    responses={200: "OK"}
)
@api_view(['POST'])
@authentication_classes([
    SessionAuthentication,
    TokenAuthentication,
    ManagerKeyAuthenticator
])
@permission_classes([IsAuthenticated, IsAdminUser])
def restaurant_menu_remove(request):
    serializer = RestaurantMenuItemsSerializer(data=request.data)

    if not serializer.is_valid():
        raise ValidationError()

    validated_data = serializer.validated_data
    restaurant = Restaurant.objects.filter(id=validated_data['id']).first()

    if restaurant is None:
        raise RestaurantNotFound()

    restaurant.menu.remove(*validated_data['items'])
    return Response({}, status=status.HTTP_200_OK)
