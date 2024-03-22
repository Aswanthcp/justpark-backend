from django.urls import path
from . import views


urlpatterns = [
    path("admin-login/", views.admin_login, name="admin_login"),
    # user logic
    path("get-users-list/", views.getUsers, name="getUsers"),
    path("get-user-byID/<int:id>", views.getUserby_id, name="getUserby_id"),
    path("block-user/<int:id>", views.BlockUsers, name="BlockUsers"),
    path("unblock-user/<int:id>", views.UnBlockUsers, name="BlockUsers"),
    # place logic
    path("get-Place-list/", views.getPlaces, name="getPlaces"),
    path("add-Place-new/", views.addparkingPlace, name="getPlaces"),
    path("get-Place-byID/<int:id>", views.getPlaceby_id, name="getPlaces"),
    # slot logic
    path("get-Parking-slot/", views.getParkingSLot, name="getParkingSLot"),
    path("book-slot/<int:id>", views.bookSlots, name="BlockUsers"),
    path("unbook-slot/<int:id>", views.UnbookSlots, name="UnbookSlots"),
    path("update-slot-price/<int:id>", views.UpdateSlotPrice, name="UpdateSlotPrice"),
    # reservations logic
    path("get-reservations-list/", views.getReservations, name="getUsers"),
    path(
        "update-reservations-status/<int:id>",
        views.update_reservation_status,
        name="update_reservation_status",
    ),
    path(
        "reservations-per-month/",
        views.reservations_per_month_chart,
        name="reservations_per_month_chart",
    ),
    path(
        "users-created-per-day/",
        views.users_created_per_day,
        name="users_created_per_day",
    ),
]
