from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("get_parkingPlace/", views.getparkingPlace, name="get_parkingPlace"),
    path("add_parkingPlace/", views.addparkingPlace, name="add_parkingPlace"),
    path("get_parkingSlot/", views.getParkingSLot, name="get_parkingSlot"),
    path("add_parkingSlot/", views.createParkingSlot, name="add_parkingSlot"),
    path(
        "get-parkingSlot-byplace/<int:id>/",
        views.getParkingSlotbyplace,
        name="add_parkingSlot",
    ),
    path(
        "get-parkingSlotby-Id/<int:id>/",
        views.getParkingSLotby_Id,
        name="get_parkingSlot_by_id",
    ),
    path(
        "Create-BookParkinSlot-byuser/",
        views.Create_BookParkinSlot_byuser,
        name="Create_BookParkinSlot_byuser",
    ),
    path(
        "create-checkout-session/",
        views.create_checkout_session,
        name="create_checkout_session",
    ),
    path(
        "getReservations/<int:id>/",
        views.get_reservationby_id,
        name="get_reservationby_id",
    ),
]
