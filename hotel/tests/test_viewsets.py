import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from hotel.models import Guest, Restaurant, Floor, MenuItemCat, MenuItem

TEST_USER = 'test'
TEST_PASS = '123456'


class UserMixin:
    user: User = None
    guest: Guest = None

    def create_user(self):
        if self.user:
            return self.user

        self.user = User.objects.create_user(TEST_USER, password=TEST_PASS)
        self.guest = Guest.objects.create(
            user=self.user,
            first_name='test',
            last_name='user',
            phone_number='093773867234',
        )
        return self.user

    def create_staff_user(self):
        if not self.user:
            self.create_user()

        self.user.is_staff = True
        self.user.save()

    def create_login(self):
        response = self.client.post(
            '/api/hotel/guest/login',
            content_type='application/json',
            data={'login': TEST_USER, 'password': TEST_PASS}
        )
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class GuestTestCase(UserMixin, TestCase):
    def setUp(self):
        self.user = User.objects.create_user(TEST_USER, password=TEST_PASS)
        self.guest = Guest.objects.create(
            user=self.user,
            first_name='test',
            last_name='user',
            phone_number='093773867234',
        )

    def test_login(self):
        response = self.client.post(
            '/api/hotel/guest/login',
            content_type='application/json',
            data={'login': TEST_USER, 'password': TEST_PASS}
        )
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        user = 'user1'
        password = 'test12345'
        response = self.client.post(
            '/api/hotel/guest/register',
            content_type='application/json',
            data={
                'login': user,
                'password': password,
                'first_name': 'vasyl',
                'last_name': 'petrenko',
                'phone_number': '380501234567',
            }
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/api/hotel/guest/login',
            content_type='application/json',
            data={'login': user, 'password': password}
        )
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.create_login()

        response = self.client.post(
            '/api/hotel/guest/logout',
        )
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class RestaurantTestCase(UserMixin, TestCase):
    def setUp(self):
        self.create_staff_user()
        self.create_login()
        self.floor = Floor.objects.create(level=1)
        self.restaurant = Restaurant.objects.create(
            floor=self.floor,
            name="Supreme Food",
        )
        self.menu_cat = MenuItemCat.objects.create(name='Sea food')
        self.menu_items = [
            MenuItem.objects.create(
                category=self.menu_cat,
                name='Shrimp',
                price=455,
            ),
            MenuItem.objects.create(
                category=self.menu_cat,
                name='Roasted Perch',
                price=200,
            ),
        ]

    def test_list(self):
        response = self.client.get('/api/hotel/restaurant/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, response.data['count'])

    def test_add_and_remove(self):
        response = self.client.post(
            '/api/hotel/restaurant/',
            content_type='application/json',
            data={
                'floor': self.floor.id,
                'name': 'Korean food',
            }
        )
        self.assertEqual(response.status_code, 201)
        restaurant_id = response.data['id']
        self.assertGreater(restaurant_id, 0)
        response = self.client.delete(f'/api/hotel/restaurant/{restaurant_id}/')
        self.assertEqual(response.status_code, 204)
        response = self.client.get(f'/api/hotel/restaurant/{restaurant_id}/')
        self.assertEqual(response.status_code, 404)

    def test_menu(self):
        response = self.client.post(
            '/api/hotel/restaurant/',
            content_type='application/json',
            data={
                'floor': self.floor.id,
                'name': 'Korean food',
            }
        )
        self.assertEqual(response.status_code, 201)
        restaurant_id = response.data['id']
        response = self.client.post(
            '/api/hotel/restaurant/menu/add',
            content_type='application/json',
            data={
                'id': restaurant_id,
                'items': [i.id for i in self.menu_items],
            }
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/api/hotel/restaurant/menu/remove',
            content_type='application/json',
            data={
                'id': restaurant_id,
                'items': [i.id for i in self.menu_items],
            }
        )
        self.assertEqual(response.status_code, 204)
