from django.urls import path
from rest_framework.routers import DefaultRouter

from hotel.views import guest
from hotel.views.employee import employee_shift_set, EmployeeViewSet
from hotel.views.floor import FloorViewSet
from hotel.views.menu_item import MenuItemViewSet
from hotel.views.menu_item_cat import MenuItemCatViewSet
from hotel.views.reservation import ReservationViewSet
from hotel.views.restaurant import RestaurantViewSet, restaurant_menu_add, \
    restaurant_menu_remove
from hotel.views.role import RoleViewSet
from hotel.views.room import RoomViewSet
from hotel.views.shift import ShiftViewSet

router = DefaultRouter()
router.register('role', RoleViewSet)
router.register('shift', ShiftViewSet)
router.register('employee', EmployeeViewSet)
router.register('menu-item-cat', MenuItemCatViewSet)
router.register('menu-item', MenuItemViewSet)
router.register('floor', FloorViewSet)
router.register('restaurant', RestaurantViewSet)
router.register('room', RoomViewSet)
router.register('reservation', ReservationViewSet)

urls = [
    path('employee/shift', employee_shift_set),
    path('restaurant/menu/add', restaurant_menu_add),
    path('restaurant/menu/remove', restaurant_menu_remove),
    path('guest/register', guest.register),
    path('guest/login', guest.login),
    path('guest/logout', guest.logout),
] + router.urls
