# Generated by Django 4.1.3 on 2022-11-18 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0006_alter_invoices_datetime_alter_orders_createed_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 10, 0, 41, 549243)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='createed_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 10, 0, 41, 549243)),
        ),
        migrations.AlterField(
            model_name='traillogs',
            name='createed_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 11, 18, 10, 0, 41, 549243)),
        ),
    ]
