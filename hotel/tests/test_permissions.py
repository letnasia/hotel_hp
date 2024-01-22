from unittest.mock import Mock
import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from hotel.permissions import IsReservationGuestOrSuperAdmin


@pytest.mark.django_db
class IsReservationGuestOrSuperAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test1')
        self.user2 = User.objects.create_user('test2')

    def test_has_object_permission(self):
        request = Mock()
        request.user = self.user
        request.META.get = Mock()
        view = Mock()
        obj = Mock()
        obj.guest = self.user
        self.assertTrue(
            IsReservationGuestOrSuperAdmin().has_object_permission(
                request,
                view,
                obj
            )
        )
