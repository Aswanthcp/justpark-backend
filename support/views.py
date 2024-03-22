from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.hashers import make_password
import jwt

from admin.utils.pagination import paginate_queryset

from django.conf import settings
from api.models import *
from api.serializers import *


def generate_jwt_token(user):
    payload = {
        "username": user.username,
        "email": user.email,
        "password": user.password,
    }
    jwt_token = jwt.encode(payload, "secret", algorithm="HS256")
    return jwt_token


@api_view(["POST"])
def support_login(request):
    try:
        data = request.data

        username = data["username"]
        password = data["password"]
        place_name = data["place_name"]

        parking_place_exists = parkingPlace.objects.filter(name=place_name).exists()

        if not parking_place_exists:
            return Response("Parking place not found", status=status.HTTP_404_NOT_FOUND)
        else:
            user = authenticate(username=username, password=password)
            serial = MyUserSerializer(user, many=False)
            if user is not None:
                if user.role == MyUser.UserRoles.SUPPORT:
                    Jwt_token = generate_jwt_token(user)
                    try:
                        support_place = SupportPlace.objects.get(user=user)
                        parking_place = support_place.parking_place
                        return Response(
                            {
                                "data": serial.data,
                                "place": parking_place.id,
                                "role": user.role,
                                "support_jwt": Jwt_token,
                            }
                        )
                    except SupportPlace.DoesNotExist:
                        return Response(
                            "User is not assigned to a parking place",
                            status=status.HTTP_403_FORBIDDEN,
                        )
                else:
                    return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(
                    "Invalid credentials", status=status.HTTP_401_UNAUTHORIZED
                )
    except Exception as e:
        return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def signup(request):
    data = request.data
    try:
        user = MyUser.objects.create(
            username=data["email"],
            email=data["email"],
            password=make_password(data["password"]),
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        user.role = MyUser.UserRoles.SUPPORT
        user.phone_number = data.get("phone_number", "")
        user.save()

        parking_place_exists = parkingPlace.objects.filter(
            name=data["parking_place_name"]
        ).exists()

        if not parking_place_exists:
            new_parking_place = parkingPlace.objects.create(
                name=data["parking_place_name"],
                address="Default address",
                total_slots=30,
            )
        else:
            new_parking_place = parkingPlace.objects.get(
                name=data["parking_place_name"]
            )

        SupportPlace.objects.create(user=user, parking_place=new_parking_place)

        serializer = MyUserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        message = {"detail": "username taken"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getUsers(request):
    data = (
        MyUser.objects.exclude(is_superuser=True).exclude(role="support").order_by("id")
    )

    page_number = request.GET.get("page", 1)
    items_per_page = 3  # Adjust as needed

    pagination_data, error, status_code = paginate_queryset(
        data, MyUserSerializer, page_number, items_per_page
    )

    if error:
        return Response(error, status=status_code)

    return Response(pagination_data, status=status_code)


from urllib.parse import unquote_plus


@api_view(["GET"])
def getReservations(request):
    support = request.GET.get("support")

    data = Reservation.objects.filter(support__username=support).order_by("id")

    # Pagination
    page_number = request.GET.get("page", 1)
    items_per_page = 3  # Adjust as needed

    pagination_data, error, status_code = paginate_queryset(
        data, ReservationViewSerializer, page_number, items_per_page
    )

    if error:
        return Response(error, status=status_code)

    return Response(pagination_data, status=status_code)


@api_view(["POST"])
def addReservations(request):
    data = request.data

    username = request.data.get("username", {})
    support_id = request.data.get("support_id", {})

    user = MyUser.objects.filter(username=username).first()
    support = MyUser.objects.get(id=support_id)
    if not user:
        user = MyUser.objects.create(
            username=data["username"],
            email=data["username"],
            password=make_password("11111111"),
            first_name="first Name",
            last_name="second Name",
            address="main address",
            phone_number=data["phone_number"],
        )
        user.role = MyUser.UserRoles.CUSTOMER
        user.save()

    slot = ParkingSlot.objects.filter(id=int(data["slot_number"])).first()

    if not slot:
        return Response({"error": "Invalid slot ID."}, status=400)
    if not slot.is_booked:
        data = {
            "user": user,
            "slot": slot,
            "time_reserved": request.data.get("time_reserved", ""),
            "car_details": request.data.get("car_details", ""),
            "car_number": request.data.get("car_number", ""),
            "phone_number": request.data.get("phone_number", ""),
            "payment_mode": "By Cash",
            "support": support,
        }

        reservation = Reservation.objects.create(**data)
        slot.is_booked = True

        slot.save()
        serializer = ReservationSerializer(reservation)

        return Response(serializer.data)
    else:
        return Response({"error": "Parking slot is already booked."}, status=400)


@api_view(["GET"])
def getParkingSlotbyplace(request, id):

    data = ParkingSlot.objects.filter(place__id=id)
    serializer = ParkingSlotSerializer(data, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def reservations_per_month_chart(request, place_id):
    if request.method == "GET":
        reservations_data = Reservation.reservations_per_month_place(place_id)
        serializer = ReservationMonthSerializer(reservations_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
