from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver

class MyUser(AbstractUser):
    class UserRoles(models.TextChoices):
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"
        SUPPORT = "support", "Support"
        CUSTOMER = "customer", "Customer"

    phone_number = models.CharField(max_length=250, unique=False)
    email = models.EmailField(default="abc@gmail.com")
    address = models.TextField(default="abc 123")
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                name="unique_email_user",
            ),
        ]

    def __str__(self) -> str:
        return self.username


class parkingPlace(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    total_slots = models.IntegerField(default=30)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        created = not self.pk

        super().save(*args, **kwargs)

        existing_slots = ParkingSlot.objects.filter(place=self)

        if created or existing_slots.count() < self.total_slots:
            for slot_number in range(existing_slots.count() + 1, self.total_slots + 1):
                ParkingSlot.objects.create(place=self, slot_number=slot_number)

        elif existing_slots.count() > self.total_slots:
            excess_slot_numbers = existing_slots.values_list("slot_number", flat=True)[
                self.total_slots :
            ]
            ParkingSlot.objects.filter(
                place=self, slot_number__in=excess_slot_numbers
            ).delete()


class ParkingSlot(models.Model):
    place = models.ForeignKey(parkingPlace, on_delete=models.CASCADE)
    slot_number = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.place.name} - Slot {self.slot_number}"


class Reservation(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("waiting", "waiting"),
    )

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    support = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="supported_reservations",
        limit_choices_to={"role": MyUser.UserRoles.SUPPORT},
        null=True,
        blank=True,
    )
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now_add=True)
    car_number = models.CharField(max_length=255, default="")
    car_details = models.CharField(max_length=255, default="")
    payment_id = models.CharField(max_length=255, default="")
    time_reserved = models.CharField(max_length=255, default="1")
    phone_number = models.CharField(max_length=250, default="0000000000")
    status = models.CharField(max_length=50, choices=STATUS, default="Pending")
    payment_mode = models.CharField(max_length=255, default="COD")

    def __str__(self):
        return f"{self.user.username} - {self.slot}"

    def delete(self, *args, **kwargs):
        self.slot.is_booked = False
        self.slot.save()
        super().delete(*args, **kwargs)


class SupportPlace(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    parking_place = models.ForeignKey(parkingPlace, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "parking_place")
        
        

@receiver(post_delete, sender=Reservation)
def update_slot_is_booked(sender, instance, **kwargs):
    instance.slot.is_booked = False
    instance.slot.save()
