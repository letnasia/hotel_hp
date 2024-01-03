from rest_framework import status
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, \
    authentication_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from hotel.authenticators import ManagerKeyAuthenticator
from hotel.exceptions import EmployeeNotFound
from hotel.models import Employee
from hotel.serializers.employee import EmployeeSerializer, \
    EmployeeWithShiftsSerializer, EmployeeShiftsSerializer


class EmployeeViewSet(ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
        ManagerKeyAuthenticator,
    )
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Employee.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmployeeWithShiftsSerializer
        else:
            return EmployeeSerializer


@api_view(['POST'])
@authentication_classes([
    SessionAuthentication,
    TokenAuthentication,
    ManagerKeyAuthenticator
])
@permission_classes([IsAuthenticated, IsAdminUser])
def employee_shift_set(request):
    serializer = EmployeeShiftsSerializer(data=request.data)

    if not serializer.is_valid():
        raise ValidationError()

    validated_data = serializer.validated_data
    employee = Employee.objects.get(id=validated_data['id'])

    if employee is None:
        raise EmployeeNotFound()

    employee.shifts.set(validated_data['shifts'])
    return Response({
        "id": validated_data['id'],
        "shifts": validated_data['shifts']
    }, status=status.HTTP_201_CREATED)
