import datetime as dt
from django.db import transaction

from google_sheets.client import write_to_sheet
from hotel.telegram_client import send_message
from hotel.models import Shift, Reservation
from hotel_hp.celery import app


@app.task()
def cleanup_shifts():
    """Cleanup shifts older than a week"""
    day_count = 7

    today = dt.date.today()
    week_behind = today - dt.timedelta(days=day_count)
    Shift.objects.filter(date__lt=week_behind).delete()


@app.task()
def populate_shifts():
    """Ensure shifts a week ahead"""
    shift_count = 3
    day_count = 7

    today = dt.date.today()
    week_ahead = today + dt.timedelta(days=day_count)

    with transaction.atomic():
        existing = {
            (ex.date, ex.number) for ex in
            Shift.objects.filter(date__gte=today, date__lt=week_ahead)
        }
        missing = [
            Shift(date=today + dt.timedelta(days=d), number=s)
            for d in range(day_count)
            for s in range(1, shift_count + 1)
            if (today + dt.timedelta(days=d), s) not in existing
        ]
        Shift.objects.bulk_create(missing)


@app.task()
def cleanup_old_reservations():
    """Cleanup reservations that have expired a week before"""
    day_count = 7

    today = dt.date.today()
    week_behind = today - dt.timedelta(days=day_count)
    Reservation.objects.filter(last_date__lt=week_behind).delete()


@app.task()
def cleanup_unpaid_reservations():
    """Cleanup unpaid reservations that have reached the deadline"""
    Reservation.objects\
        .filter(is_paid=False, pay_deadline__lt=dt.datetime.now())\
        .delete()


@app.task()
def reservation_created(reservation_id):
    """Notify about a new reservation"""
    reservation = Reservation.objects.get(id=reservation_id)
    start_date = reservation.get_start_date()
    rooms = reservation.get_unique_rooms()
    guests = sum(r.accommodation for r in rooms)
    send_message(
        f"New reservation {reservation.id} from  {start_date}"
        f" till {reservation.end_date} for {rooms.count()} rooms"
        f" and {guests} guests"
    )


@app.task()
def reservation_daily_stats():
    """Report about daily reservation stats"""
    today = dt.date.today()
    yesterday = today - dt.timedelta(days=1)

    reservations = Reservation.objects.filter(
        created_at__gte=yesterday,
        created_at__lt=today
    )
    rows = []

    for reservation in reservations:
        start_date = reservation.get_start_date()
        rooms = reservation.get_unique_rooms()
        guests = sum(r.accommodation for r in rooms)
        rows.append([
            str(reservation.id),
            reservation.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            str(start_date),
            str(reservation.end_date),
            str(rooms.count()),
            str(guests)
        ])

    write_to_sheet("Hotel HP", rows)

