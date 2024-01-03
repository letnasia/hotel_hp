from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from hotel.authenticators import ManagerKeyAuthenticator
from hotel.models import Shift
from hotel.serializers.shift import ShiftSerializer


class ShiftViewSet(ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
        ManagerKeyAuthenticator,
    )
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = ShiftSerializer
    queryset = Shift.objects.all()
