# Generated by Django 4.1.3 on 2022-11-18 09:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0005_alter_invoices_datetime_alter_orders_createed_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 9, 47, 23, 325877)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='createed_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 9, 47, 23, 325877)),
        ),
    ]
