# razorpay.py

import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_order(amount):
    data = {
        "amount": amount * 100,
        "currency": "INR",
        "payment_capture": "1",
    }
    order = client.order.create(data)
    return order
