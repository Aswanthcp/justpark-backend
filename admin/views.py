from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.hashers import make_password
import jwt
from django.core.paginator import Paginator

from django.conf import settings
from .utils.pagination import paginate_queryset
from api.models import *
from api.serializers import *


@api_view(["POST"])
def admin_login(request):
    try:
        data = request.data

        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        serial = MyUserSerializer(user, many=False)
        print(user)
        if user is not None:
            if user.role == MyUser.UserRoles.ADMIN and user.is_superuser:
                jwt_token = generate_jwt_token(user)

                return Response({"admin": serial.data, "admin_jwt": jwt_token})
            elif user.role == MyUser.UserRoles.STAFF:
                jwt_token = generate_jwt_token(user)
                return Response({"data": serial.data, "staff_jwt": jwt_token})
            elif user.role == MyUser.UserRoles.SUPPORT:
                jwt_token = generate_jwt_token(user)
                return Response(
                    {"data": serial.data, "role": user.role, "support_jwt": jwt_token}
                )

            else:
                return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)


def generate_jwt_token(user):
    payload = {
        "username": user.username,
        "email": user.email,
        "password": user.password,
    }
    jwt_token = jwt.encode(payload, "secret", algorithm="HS256")
    return jwt_token


@api_view(["GET"])
def getUsers(request):
    data = MyUser.objects.all().exclude(is_superuser=True)
    page_number = request.GET.get("page", 1)
    items_per_page = 3  # Adjust as needed

    pagination_data, error, status_code = paginate_queryset(
        data, MyUserSerializer, page_number, items_per_page
    )

    if error:
        return Response(error, status=status_code)

    return Response(pagination_data, status=status_code)


@api_view(["GET"])
def getUserby_id(request, id):
    data = MyUser.objects.get(id=id)
    serial = MyUserSerializer(data, many=False)
    return Response(serial.data)


@api_view(["PATCH"])
def BlockUsers(request, id):
    try:
        user = MyUser.objects.get(id=id)
    except MyUser.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)

    user.is_active = False  # Assuming setting is_active to False blocks the user
    user.save()

    data = MyUser.objects.all().exclude(is_superuser=True)
    page_number = request.GET.get("page", 1)
    items_per_page = 3

    pagination_data, error, status_code = paginate_queryset(
        data, MyUserSerializer, page_number, items_per_page
    )

    if error:
        return Response(error, status=status_code)

    return Response(pagination_data, status=status_code)


@api_view(["PATCH"])
def UnBlockUsers(request, id):
    try:
        user = MyUser.objects.get(id=id)
    except MyUser.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)

    user.is_active = True  # Assuming setting is_active to False blocks the user
    user.save()

    data = MyUser.objects.all().exclude(is_superuser=True)
    page_number = request.GET.get("page", 1)
    items_per_page = 3

    pagination_data, error, status_code = paginate_queryset(
        data, MyUserSerializer, page_number, items_per_page
    )

    if error:
        return Response(error, status=status_code)

    return Response(pagination_data, status=status_code)


# Place view


@api_view(["GET"])
def getPlaces(request):
    data = parkingPlace.objects.all()
    page_number = request.GET.get("page", 1)
    items_per_page = 3  # Adjust as needed

    pagination_data, error, status_code = paginate_queryset(
        data, parkingPlaceSerializer, page_number, items_per_page
    )

    if error:
        return Response(error, status=status_code)

    return Response(pagination_data, status=status_code)


@api_view(["GET", "PUT"])
def getPlaceby_id(request, id):
    try:
        data = parkingPlace.objects.get(pk=id)

    except parkingPlace.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = parkingPlaceSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serial = parkingPlaceSerializer(data, many=False)
    return Response(serial.data)


@api_view(["POST"])
def addparkingPlace(request):
    serializer = parkingPlaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=201)


# slot view


@api_view(["GET"])
def getParkingSLot(request):
    data = ParkingSlot.objects.all()
    page_number = request.GET.get("page", 1)
    items_per_page = 8  # Adjust as needed

    pagination_data, error, status_code = paginate_queryset(
        data, ParkingSlotViewSerializer, page_number, items_per_page
    )

    if error:
        return Response(error, status=status_code)

    return Response(pagination_data, status=status_code)


@api_view(["PATCH"])
def bookSlots(request, id):
    try:
        data_ = ParkingSlot.objects.get(id=id)
    except MyUser.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)

    data_.is_booked = False  # Assuming setting is_active to False blocks the user
    data_.save()

    data = ParkingSlot.objects.all()
    page_number = request.GET.get("page", 1)
    items_per_page = 3

    pagination_data, error, status_code = paginate_queryset(
        data, ParkingSlotViewSerializer, page_number, items_per_page
    )

    if error:
        return Response(error, status=status_code)

    return Response(pagination_data, status=status_code)


@api_view(["PATCH"])
def UnbookSlots(request, id):
    try:
        data_ = ParkingSlot.objects.get(id=id)
    except MyUser.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)

    data_.is_booked = True  # Assuming setting is_active to False blocks the user
    data_.save()

    data = ParkingSlot.objects.all()
    page_number = request.GET.get("page", 1)
    items_per_page = 3

    pagination_data, error, status_code = paginate_queryset(
        data, ParkingSlotViewSerializer, page_number, items_per_page
    )

    if error:
        return Response(error, status=status_code)

    return Response(pagination_data, status=status_code)


from django.core.exceptions import ObjectDoesNotExist


@api_view(["PATCH"])
def UpdateSlotPrice(request, id):
    try:
        slot = ParkingSlot.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response("Slot not found", status=status.HTTP_404_NOT_FOUND)

    try:
        new_price = float(request.data["price"])  # Convert price to float
    except (KeyError, ValueError):
        return Response("Invalid price format", status=status.HTTP_400_BAD_REQUEST)

    # Update the price of the slot
    slot.price = new_price
    slot.save()

    # Get all slots for pagination
    data = ParkingSlot.objects.all()
    page_number = request.GET.get("page", 1)
    items_per_page = 3

    pagination_data, error, status_code = paginate_queryset(
        data, ParkingSlotViewSerializer, page_number, items_per_page
    )

    if error:
        return Response(error, status=status_code)

    return Response(pagination_data, status=status_code)


@api_view(["GET"])
def getReservations(request):

    data = Reservation.objects.all()
    page_number = request.GET.get("page", 1)
    items_per_page = 5

    pagination_data, error, status_code = paginate_queryset(
        data, ReservationViewSerializer, page_number, items_per_page
    )

    if error:
        return Response(error, status=status_code)

    return Response(pagination_data, status=status_code)


@api_view(["PUT"])
def update_reservation_status(request, id):
    try:
        # Retrieve the reservation object
        reservation = Reservation.objects.get(id=id)

        # Get the new status from the request data
        new_status = request.data.get("status")

        # Update the status of the reservation
        reservation.status = new_status
        reservation.save()

        # Serialize the updated reservation
        serializer = ReservationSerializer(reservation)

        # Return success response with updated reservation data
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Reservation.DoesNotExist:
        # If reservation does not exist, return error response
        return Response(
            {"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        # Handle other exceptions
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def reservations_per_month_chart(request):
    if request.method == "GET":
        reservations_data = Reservation.reservations_per_month()
        serializer = ReservationMonthSerializer(reservations_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def users_created_per_day(request):
    if request.method == 'GET':
        user_data = MyUser.objects.values('date_joined__date').annotate(count=Count('id'))
        formatted_data = [{'date': entry['date_joined__date'], 'count': entry['count']} for entry in user_data]
        return Response(formatted_data)