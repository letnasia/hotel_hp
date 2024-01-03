from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from hotel.authenticators import ManagerKeyAuthenticator
from hotel.models import Floor
from hotel.serializers.floor import FloorSerializer


class FloorViewSet(ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
        ManagerKeyAuthenticator,
    )
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = FloorSerializer
    queryset = Floor.objects.all()

