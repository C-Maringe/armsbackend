from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


def two_hours_hence():
    return timezone.now() + timezone.timedelta(hours=0)


class employees(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="OFFLINE")
    lastname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    employee_status = models.CharField(max_length=100, default="ACTIVE")
    supervisorcode = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, default="TELLER")
    username = models.CharField(max_length=100)


class invoices(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(default=two_hours_hence, blank=False)
    status = models.CharField(max_length=100, null=True, blank=True)
    amount = models.BigIntegerField(blank=True, null=True)
    vat = models.BigIntegerField(blank=True, null=True)
    currency = models.CharField(max_length=100, null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    channel = models.CharField(max_length=100, null=True, blank=True)
    employeeId = models.BigIntegerField()


class rates(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=10, unique=True,null=True)
    rate = models.DecimalField(max_digits=15, decimal_places=5)


class BaseCurrency(models.Model):
    id = models.AutoField(primary_key=True)
    base_currency = models.ForeignKey(rates, on_delete=models.CASCADE, related_name='base_currency')


class sales(models.Model):
    id = models.AutoField(primary_key=True)
    base_currency = models.CharField(max_length=100, blank=True)
    channel = models.CharField(max_length=100, blank=True)
    cost_price = models.BigIntegerField(null=True)
    datetime = models.DateTimeField(default=two_hours_hence)
    employeeId = models.BigIntegerField(null=True)
    product = models.CharField(max_length=1000)
    price = models.BigIntegerField(null=True)
    description = models.CharField(max_length=100, blank=True)
    employee = models.CharField(max_length=100, blank=True)
    foreign_currency = models.CharField(max_length=100, blank=True)
    imei = models.CharField(max_length=100, null=True, blank=True)
    invoiceId = models.BigIntegerField(null=True)
    pan = models.CharField(max_length=100, null=True, blank=True)
    productId = models.BigIntegerField(null=True)
    quantity = models.BigIntegerField(null=True)
    rate = models.BigIntegerField(null=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    rrn = models.CharField(max_length=100, null=True, blank=True)
    shop_name = models.CharField(max_length=100, blank=True)
    tax = models.BigIntegerField(null=True)
    total = models.BigIntegerField(null=True)
    status = models.CharField(max_length=100, blank=True)


class suppliers(models.Model):
    id = models.AutoField(primary_key=True)
    suppliers_name = models.CharField(max_length=100)
    suppliers_phone = models.CharField(max_length=100)
    suppliers_address = models.CharField(max_length=100)


class categories(models.Model):
    id = models.AutoField(primary_key=True)
    categories_id = models.IntegerField(default=1)
    categories_type = models.CharField(max_length=100)
    categories_description = models.CharField(max_length=100)

    def __str__(self):
        return self.categories_type


class products(models.Model):
    id = models.AutoField(primary_key=True)
    barcode = models.CharField(max_length=100, null=True, blank=True)
    cost = models.BigIntegerField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.BigIntegerField(null=True, blank=True)
    quantity = models.BigIntegerField(null=True, blank=True)
    tax = models.BigIntegerField(null=True, blank=True)
    order_level = models.BigIntegerField(default=20)
    categories_id = models.ForeignKey(
        categories, on_delete=models.CASCADE, default=1, null=True, blank=True)
    suppliers_id = models.ForeignKey(
        suppliers, on_delete=models.CASCADE, default=1, null=True, blank=True)


class orders(models.Model):
    id = models.AutoField(primary_key=True)
    createed_at = models.DateTimeField(default=two_hours_hence)
    cost = models.BigIntegerField()
    description = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.BigIntegerField()
    quantity = models.BigIntegerField()
    tax = models.BigIntegerField(null=True, blank=True)
    categories_id = models.ForeignKey(
        categories, on_delete=models.CASCADE, default=1, null=True, blank=True)
    suppliers_id = models.ForeignKey(
        suppliers, on_delete=models.CASCADE, default=1, null=True, blank=True)


class returnedproducts(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(default=two_hours_hence)
    quantity = models.BigIntegerField(null=True, blank=True)
    categories_id = models.ForeignKey(
        categories, on_delete=models.CASCADE, default=1, null=True, blank=True)
    suppliers_id = models.ForeignKey(
        suppliers, on_delete=models.CASCADE, default=1, null=True, blank=True)
    sales_id = models.ForeignKey(
        sales, on_delete=models.CASCADE, default=1, null=True, blank=True)


class ordersandproducts(models.Model):
    id = models.AutoField(primary_key=True)
    barcode = models.CharField(max_length=100)
    categoryId = models.BigIntegerField()
    cost = models.BigIntegerField()
    description = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.BigIntegerField()
    quantity = models.BigIntegerField()
    supplierId = models.BigIntegerField()
    tax = models.BigIntegerField()
    categories_id = models.ForeignKey(
        categories, on_delete=models.CASCADE, default=3)
    suppliers_id = models.ForeignKey(
        suppliers, on_delete=models.CASCADE, default=3)


class traillogs(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    user_id = models.BigIntegerField()
    item = models.CharField(max_length=1000)
    action = models.CharField(max_length=100)
    quantity = models.BigIntegerField()
    description = models.CharField(max_length=100)
    createed_at = models.DateTimeField(default=two_hours_hence)


class Poisonous(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=1000)
