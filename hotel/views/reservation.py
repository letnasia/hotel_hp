from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from hotel.models import Reservation
from hotel.permissions import IsReservationGuestOrSuperAdmin
from hotel.serializers.reservation import ReservationSerializer, ReservationViewSerializer


class ReservationViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsReservationGuestOrSuperAdmin,)
    queryset = Reservation.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReservationViewSerializer
        else:
            return ReservationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(guests__id=self.request.user)
