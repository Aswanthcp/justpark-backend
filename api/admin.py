from django.contrib import admin

from .models import *


admin.site.register(parkingPlace)
admin.site.register(ParkingSlot)
admin.site.register(Reservation)
admin.site.register(MyUser)
admin.site.register(SupportPlace)