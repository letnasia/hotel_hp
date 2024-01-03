from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from hotel.authenticators import ManagerKeyAuthenticator
from hotel.models import Room
from hotel.serializers.room import RoomSerializer


class RoomViewSet(ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
        ManagerKeyAuthenticator,
    )
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def get_permission_classes(self, request):
        if request.method == 'GET':
            return IsAuthenticated,
        return IsAuthenticated, IsAdminUser
