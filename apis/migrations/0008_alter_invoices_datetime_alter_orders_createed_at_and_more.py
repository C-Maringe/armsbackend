# Generated by Django 4.1.3 on 2022-11-18 10:09

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0007_alter_invoices_datetime_alter_orders_createed_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 10, 9, 11, 380901)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='createed_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 10, 9, 11, 383899)),
        ),
        migrations.AlterField(
            model_name='traillogs',
            name='createed_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
