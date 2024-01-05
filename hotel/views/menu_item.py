from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from hotel.authenticators import ManagerKeyAuthenticator
from hotel.filters import MenuItemFilter
from hotel.models import MenuItem
from hotel.serializers.menu_item import MenuItemSerializer


class ItemPagination(CursorPagination):
    ordering = '-id'


class MenuItemViewSet(ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
        ManagerKeyAuthenticator,
    )
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = MenuItemSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = MenuItemFilter

    pagination_class = ItemPagination
    ordering_fields = ('name', 'price')
    ordering = ('name',)

    queryset = MenuItem.objects.all()

