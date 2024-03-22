from django.urls import path
from . import views


urlpatterns = [
    path("support-login/", views.support_login, name="support_login"),
    path("support-signup/", views.signup, name="signup"),
    path("get-users-list/", views.getUsers, name="getUsers"),
    path("get-booking-list/", views.getReservations, name="getReservations"),
    path("add-new-reservations/", views.addReservations, name="addReservations"),
    path(
        "get-slot-byPlace/<int:id>",
        views.getParkingSlotbyplace,
        name="getParkingSlotbyplace",
    ),
    path(
        "reservations-per-month/<int:place_id>",
        views.reservations_per_month_chart,
        name="reservations_per_month_chart",
    ),
]
