from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.hashers import make_password
import jwt
from .razorpay import create_order
import razorpay
from django.conf import settings

from .models import *
from .serializers import *


# client section


@api_view(["POST"])
def signup(request):
    data = request.data
    print(data)

    try:
        user = MyUser.objects.create(
            username=data["email"],
            email=data["email"],
            password=make_password(data["password"]),
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        user.role = MyUser.UserRoles.CUSTOMER
        user.save()
        serializer = MyUserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        message = {"detail": "username taken"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    try:
        user = authenticate(request, username=username, password=password)

        serial = MyUserSerializer(user, many=False)
        if user:
            payload = {
                "username": username,
                "email": user.email,
                "password": user.password,
            }
            jwt_token = jwt.encode(payload, "secret", algorithm="HS256")
            return Response({"data": serial.data, "user_jwt": jwt_token})
        else:
            message = {"message": "Invalid credentials"}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        message = {"message": "Invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def getparkingPlace(request):
    data = parkingPlace.objects.all()
    serializer = parkingPlaceSerializer(data, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def addparkingPlace(request):
    serializer = parkingPlaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=201)


@api_view(["GET"])
def getParkingSLot(request):
    data = ParkingSlot.objects.all()
    serializer = ParkingSlotSerializer(data, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getParkingSLotby_Id(request, id):
    data = ParkingSlot.objects.get(pk=id)
    serializer = ParkingSlotViewSerializer(data, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def createParkingSlot(request):
    serializer = ParkingSlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=201)


@api_view(["GET"])
def getParkingSlotbyplace(request, id):
    data = ParkingSlot.objects.filter(place__id=id)
    serializer = ParkingSlotSerializer(data, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_reservationby_id(request, id):

    data = Reservation.objects.filter(user__id=id)
    serializer = ReservationSerializer(data, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_checkout_session(request):

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
    amount = 1
    session = client.order.create(
        {
            "amount": amount * 100,
            "currency": "INR",
            "payment_capture": "1",
        }
    )
    order_id = session["id"]

    response_data = {
        "key": settings.RAZORPAY_KEY_ID,
        "amount": session["amount"],
        "currency": session["currency"],
        "order_id": order_id,
    }
    return Response({"payment": response_data})


@api_view(["POST"])
def Create_BookParkinSlot_byuser(request):
    user_id = request.data.get("user", {}).get("id")

    if not user_id:
        return Response({"error": "User ID is required."}, status=400)

    user = MyUser.objects.filter(id=user_id).first()

    if not user:
        return Response({"error": "Invalid user ID."}, status=400)

    slot_id = request.data.get("slot", {}).get("id")
    slot = ParkingSlot.objects.filter(id=slot_id).first()

    if not slot:
        return Response({"error": "Invalid slot ID."}, status=400)
    if not slot.is_booked:
        data = {
            "user": user,
            "slot": slot,
            "time_reserved": request.data.get("reservation_time"),
            "car_details": request.data.get("car_details"),
            "car_number": request.data.get("car_number"),
            "payment_id": str(request.data.get("payment_id")),
        }

        reservation = Reservation.objects.create(**data)
        slot.is_booked = True
        slot.save()
        serializer = ReservationSerializer(reservation)

        return Response(serializer.data)
    else:
        return Response({"error": "Parking slot is already booked."}, status=400)
