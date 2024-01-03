from rest_framework.exceptions import APIException


class EmployeeNotFound(APIException):
    status_code = 400
    default_detail = 'Employee does not exist'
    default_code = 'employee_not_found'


class RestaurantNotFound(APIException):
    status_code = 400
    default_detail = 'Restaurant does not exist'
    default_code = 'restaurant_not_found'


class RoomNotFound(APIException):
    status_code = 400
    default_detail = 'Room does not exist'
    default_code = 'room_not_found'


class RoomAlreadyReserved(APIException):
    status_code = 400
    default_detail = 'Room is already reserved on some of the selected dates'
    default_code = 'room_already_reserved'


class DateFromPast(APIException):
    status_code = 400
    default_detail = 'Specified date is from the past'
    default_code = 'date_from_past'


class ReserveLimit(APIException):
    status_code = 400
    default_detail = 'Room reservation limit violated'
    default_code = 'reserve_limit'


class UserExists(APIException):
    status_code = 400
    default_detail = 'Such user already exists'
    default_code = 'user_exists'


class InvalidCredentials(APIException):
    status_code = 400
    default_detail = 'No such user or password'
    default_code = 'invalid_credentials'
