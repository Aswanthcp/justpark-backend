# Generated by Django 5.0.2 on 2024-03-08 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_reservation_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='time_reserved',
            field=models.CharField(default='1', max_length=255),
        ),
    ]
