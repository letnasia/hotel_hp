from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from hotel.authenticators import ManagerKeyAuthenticator
from hotel.filters import RoomFilter
from hotel.models import Room
from hotel.serializers.room import RoomSerializer


class RoomPagination(CursorPagination):
    ordering = '-id'


class RoomViewSet(ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
        ManagerKeyAuthenticator,
    )
    serializer_class = RoomSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = RoomFilter

    pagination_class = RoomPagination
    ordering_fields = ('accommodation', 'price')
    ordering = ('accommodation',)

    queryset = Room.objects.all()

    def get_permission_classes(self, request):
        if request.method == 'GET':
            return IsAuthenticated,
        return IsAuthenticated, IsAdminUser
