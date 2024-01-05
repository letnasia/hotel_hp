import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from hotel.models import Role, Employee, Shift, MenuItemCat, MenuItem, Floor, \
    Restaurant, Room, Guest, Reservation


class RoleNode(DjangoObjectType):
    class Meta:
        model = Role
        filter_fields = ['name']
        interfaces = (relay.Node,)


class EmployeeNode(DjangoObjectType):
    class Meta:
        model = Employee
        filter_fields = ['first_name', 'last_name', 'role', 'shifts']
        interfaces = (relay.Node,)


class ShiftNode(DjangoObjectType):
    class Meta:
        model = Shift
        filter_fields = ['date', 'number']
        interfaces = (relay.Node,)


class MenuItemCatNode(DjangoObjectType):
    class Meta:
        model = MenuItemCat
        filter_fields = ['name']
        interfaces = (relay.Node,)


class MenuItemNode(DjangoObjectType):
    class Meta:
        model = MenuItem
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith'],
            'price': ['exact'],
        }
        fields = ['category', 'name', 'price', 'description']
        interfaces = (relay.Node,)


class FloorNode(DjangoObjectType):
    class Meta:
        model = Floor
        filter_fields = ['level']
        interfaces = (relay.Node,)


class RestaurantNode(DjangoObjectType):
    class Meta:
        model = Restaurant
        filter_fields = ['floor', 'name', 'menu']
        interfaces = (relay.Node,)


class RoomNode(DjangoObjectType):
    class Meta:
        model = Room
        filter_fields = {
            'description': ['exact', 'icontains', 'istartswith'],
            'floor': ['exact'],
            'accommodation': ['exact'],
            'price': ['exact'],
        }
        fields = [
            'floor',
            'size',
            'accommodation',
            'description',
            'price'
        ]
        interfaces = (relay.Node,)


class GuestNode(DjangoObjectType):
    class Meta:
        model = Guest
        filter_fields = [
            'first_name',
            'last_name',
            'phone_number',
            'created_at'
        ]
        interfaces = (relay.Node,)


class ReservationNode(DjangoObjectType):
    class Meta:
        model = Reservation
        filter_fields = [
            'guest',
            'created_at',
            'is_paid',
            'pay_deadline',
            'end_date',
            'rooms',
        ]
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    role = relay.Node.Field(RoleNode)
    all_roles = DjangoFilterConnectionField(RoleNode)

    employee = relay.Node.Field(EmployeeNode)
    all_employees = DjangoFilterConnectionField(EmployeeNode)

    shift = relay.Node.Field(ShiftNode)
    all_shifts = DjangoFilterConnectionField(ShiftNode)

    menu_item_cat = relay.Node.Field(MenuItemCatNode)
    all_menu_item_cats = DjangoFilterConnectionField(MenuItemCatNode)

    menu_item = relay.Node.Field(MenuItemNode)
    all_menu_items = DjangoFilterConnectionField(MenuItemNode)

    floor = relay.Node.Field(FloorNode)
    all_floors = DjangoFilterConnectionField(FloorNode)

    restaurant = relay.Node.Field(RestaurantNode)
    all_restaurants = DjangoFilterConnectionField(RestaurantNode)

    room = relay.Node.Field(RoomNode)
    all_rooms = DjangoFilterConnectionField(RoomNode)

    guest = relay.Node.Field(GuestNode)
    all_guests = DjangoFilterConnectionField(GuestNode)

    reservation = relay.Node.Field(ReservationNode)
    all_reservations = DjangoFilterConnectionField(ReservationNode)


schema = graphene.Schema(query=Query)
