from rest_framework import serializers
from django.db import transaction
import datetime as dt

from hotel.exceptions import RoomAlreadyReserved, RoomNotFound, DateFromPast, ReserveLimit
from hotel.models import Reservation, RoomReserve, Room
from hotel.serializers.guest import GuestSerializer
from hotel.serializers.room import RoomSerializer


class ReservationViewSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    guests = GuestSerializer(many=True)
    rooms = RoomSerializer(many=True)

    def get_start_date(self, reservation):
        return RoomReserve.objects.all()\
                .filter(reservation_id=reservation.id)\
                .order_by('date')[0].date

    class Meta:
        model = Reservation
        fields = (
            'id',
            'created_at',
            'is_paid',
            'pay_deadline',
            'start_date',
            'end_date',
            'guests',
            'rooms'
        )


class ReservationSerializer(serializers.ModelSerializer):
    PAY_DEADLINE = dt.timedelta(days=14)
    RESERVE_LIMIT_DAYS = 28

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    start_date = serializers.DateField()
    rooms = serializers.IntegerField(many=True)

    def create(self, validated_data):
        user = validated_data['user']
        room_ids = validated_data['rooms']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        self.check_dates(start_date, end_date)
        self.check_rooms_exist(room_ids)
        self.check_rooms_reserved(room_ids, start_date, end_date)
        dates = (
            start_date + dt.timedelta(i)
            for i in range((end_date - start_date).days)
        )

        with transaction.atomic():
            reservation = Reservation.objects.create(
                guest_id=user.id,
                pay_deadline=self.get_pay_deadline(start_date),
                end_date=end_date,
            )
            for room_id in room_ids:
                for date in dates:
                    RoomReserve.objects.create(
                        reservation_id=reservation.id,
                        room_id=room_id,
                        date=date,
                    )
        return reservation

    def check_dates(self, start_date: dt.date, end_date: dt.date):
        now = dt.datetime.now()
        if start_date < now.date():
            raise DateFromPast()
        if (end_date - start_date).days > self.RESERVE_LIMIT_DAYS:
            raise ReserveLimit()

    def check_rooms_exist(self, room_ids: list):
        if Room.objects.all().filter(id__in=room_ids).count() != len(room_ids):
            raise RoomNotFound()

    def check_rooms_reserved(self, room_ids: list, start_date, end_date):
        for room_id in room_ids:
            reserves = \
                RoomReserve\
                .objects.all()\
                .filter(room_id=room_id, date__ge=start_date, date__le=end_date)\
                .count()

            if reserves > 0:
                raise RoomAlreadyReserved()

    def get_pay_deadline(self, start_date: dt.datetime):
        now = dt.datetime.now()
        pay_deadline = start_date - self.PAY_DEADLINE

        if now < pay_deadline:
            # There's still a lot of time before the start_date.
            return dt.datetime(*pay_deadline.timetuple()[:3], 12)
        # There's not enough time before the start_date, reserve for 1h.
        return now + dt.timedelta(hours=1)

    class Meta:
        model = Reservation
        fields = (
            'user',
            'start_date',
            'end_date',
            'guests',
            'rooms'
        )
