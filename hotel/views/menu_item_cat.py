from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from hotel.authenticators import ManagerKeyAuthenticator
from hotel.models import MenuItemCat
from hotel.serializers.menu_item_cat import MenuItemCatSerializer


class MenuItemCatViewSet(ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
        ManagerKeyAuthenticator,
    )
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = MenuItemCatSerializer
    queryset = MenuItemCat.objects.all()

