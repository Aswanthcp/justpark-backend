from rest_framework import serializers

from .models import *


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "is_active",
        ]


class parkingPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = parkingPlace
        fields = "__all__"


class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = "__all__"


class ParkingSlotViewSerializer(serializers.ModelSerializer):
    place = parkingPlaceSerializer(read_only=True)

    class Meta:
        model = ParkingSlot
        fields = ["id", "place", "slot_number", "price", "is_booked"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class ReservationViewSerializer(serializers.ModelSerializer):
    slot = ParkingSlotSerializer(read_only=True)
    user = MyUserSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "slot",
            "user",
            "car_number",
            "time_reserved",
            "reservation_time",
            "car_details",
            "payment_id",
            "phone_number",
            "status",
        ]


class ReservationMonthSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    count = serializers.IntegerField()
