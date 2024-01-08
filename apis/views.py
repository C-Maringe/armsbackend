import hashlib
import hmac

from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view
from email import message
from rest_framework.views import APIView, Response

import datetime
import base64
import hashlib
import hmac

DECODE_KEY = b'Doctorcm@1'
from apis.serializers import (Traillogs, Employees2Serializer, ViewSalesSerializer, ProductsanCategoriesSerializer,
                              ProductsSerializer, SalesSerializer, Products2Serializer, ReturnsSerializerNew,
                              RatesSerializer, RatesUpdateSerializer, InvoicesSerializer, OrdersSerializerNew,
                              ViewSuppliersSerializer, ViewCategoriesSerializer, Suppliers1SerializerNew,
                              OrdersSerializerNew1,
                              ProductsUpdateSerializer, Employees1Serializer, EmployeesSerializer,
                              EndOfDayReconciliations,
                              ReturnsSerializerNew1, PoisonousSerializer, BaseCurrencySerializer,
                              GetBaseCurrencySerializer)
from apis.models import traillogs, categories, invoices, products, employees, rates, sales, suppliers, orders, \
    returnedproducts, Poisonous, BaseCurrency
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.db import connection
from django.shortcuts import render
import numpy as np
from time import sleep


class ViewSuppliers(ListAPIView):
    def get(self, format=None):
        emdata = suppliers.objects.all()
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "no suppliers found"})
        else:
            serializer = ViewSuppliersSerializer(emdata, many=True)
            return Response({"status": 200, "message": "Success", "suppliers": serializer.data})


class CreateSuppliers(CreateAPIView):
    queryset = suppliers.objects.all()
    serializer_class = ViewSuppliersSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": 200, "message": "Success", "suppliers": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)


class CreateExchangeCurrency(CreateAPIView):
    queryset = rates.objects.all()
    serializer_class = RatesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": 200, "message": "Success", "suppliers": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)


class BaseCurrencyView(APIView):
    serializer_class = BaseCurrencySerializer
    get_serializer_class = GetBaseCurrencySerializer

    def get(self, request):
        try:
            base_currency = BaseCurrency.objects.get()
            serializer = self.get_serializer_class(base_currency)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BaseCurrency.DoesNotExist:
            return Response({'message': 'Base currency not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check if a base currency row already exists
            try:
                base_currency = BaseCurrency.objects.get()
                serializer.update(base_currency, serializer.validated_data)
            except BaseCurrency.DoesNotExist:
                serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            base_currency = BaseCurrency.objects.get()
            base_currency.delete()
            return Response({'message': 'Base currency deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except BaseCurrency.DoesNotExist:
            return Response({'message': 'Base currency not found'}, status=status.HTTP_404_NOT_FOUND)


class CreateSuppliersNew(CreateAPIView):
    queryset = suppliers.objects.all()
    serializer_class = Suppliers1SerializerNew

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": 200, "message": "Success", "suppliers": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)


class ViewCategories(ListAPIView):
    def get(self, format=None):
        emdata = categories.objects.all()
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "no categories found"})
        else:
            serializer = ViewCategoriesSerializer(emdata, many=True)
            return Response({"status": 200, "message": "Success", "categories": serializer.data})


class CreateCategories(CreateAPIView):
    queryset = categories.objects.all()
    serializer_class = ViewCategoriesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": 200, "message": "Success", "categories": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)


class EmployeeManagement(ListAPIView):
    queryset = employees.objects.all()
    serializer_class = Employees2Serializer


class loginViewSet(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        emdata = employees.objects.filter(
            Q(firstname__icontains=username) & Q(password__icontains=password))
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "Invalid User Credidentials"})
        else:
            serializer = Employees1Serializer(emdata, many=True)
            return Response({"status_code": 200, "message": "Success", "user": serializer.data})


class ListSalesAPIView(APIView):
    def post(self, request, format=None):
        startdate = request.data.get('startdate')
        enddate = request.data.get('enddate')
        emdata = sales.objects.raw(
            'SELECT * FROM apis_sales WHERE datetime >= "' + startdate + '" AND datetime < "' + enddate + '"')
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "No Sales"})
        else:
            serializer = ViewSalesSerializer(emdata, many=True)
            return Response({"status_code": 200, "message": "Success", "sales": serializer.data})


class quantityAPIView(APIView):
    def get(self, request, format=None):
        emdata = products.objects.raw(
            'select id, quantity from apis_products')
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "No Sales"})
        else:
            serializer = ProductsUpdateSerializer(emdata, many=True)
            return Response({"status_code": 200, "message": "Success", "data": serializer.data})


class Ratesviews(ListAPIView):
    def get(self, format=None):
        emdata = rates.objects.all()
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "no rates found"})
        else:
            serializer = RatesSerializer(emdata, many=True)
            return Response({"status": 200, "message": "Success", "rates": serializer.data})


class OutOfStockProducts(ListAPIView):
    def get(self, format=None):
        emdata = products.objects.raw(
            'SELECT * FROM apis_products WHERE quantity < order_level')
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "no rates found"})
        else:
            serializer = ProductsanCategoriesSerializer(emdata, many=True)
            return Response({"status": 200, "message": "Success", "outofstock": serializer.data})


class RatesviewsZWL(ListAPIView):
    def get(self, format=None):
        emdata = rates.objects.raw(
            'SELECT * FROM apis_rates WHERE currency = "ZWL"')
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "no rates found"})
        else:
            serializer = RatesSerializer(emdata, many=True)
            return Response({"status": 200, "message": "Success", "rates": serializer.data})


class RatesCreateviews(CreateAPIView):
    queryset = rates.objects.all()
    serializer_class = RatesUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListSalesAPICreate(CreateAPIView):
    queryset = sales.objects.all()
    serializer_class = SalesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['POST'])
def update_all_items(request):
    data = request.data
    for i in data:
        id = i.get('id')
        quantity = i.get('quantity')
        update = products.objects.get(id=id)
        update.quantity -= quantity
        update.save()
    return Response({"message": "Success"})


@api_view(['POST'])
def update_categories_items(request):
    data = request.data
    for i in data:
        id = i.get('id')
        categories_type = i.get('categories_type')
        categories_description = i.get('categories_description')
        update = categories.objects.get(id=id)
        update.categories_type = categories_type
        update.categories_description = categories_description
        update.save()
    return Response({"message": "Success"})


@api_view(['POST'])
def update_suppliers_items(request):
    data = request.data
    for i in data:
        id = i.get('id')
        suppliers_name = i.get('suppliers_name')
        suppliers_phone = i.get('suppliers_phone')
        suppliers_address = i.get('suppliers_address')
        update = suppliers.objects.get(id=id)
        update.suppliers_name = suppliers_name
        update.suppliers_phone = suppliers_phone
        update.suppliers_address = suppliers_address
        update.save()
    return Response({"message": "Success"})


# CreateSuppliers


@api_view(['POST'])
def update_exchangerate_items(request):
    data = request.data
    for i in data:
        id = i.get('id')
        baseCurrency = i.get('baseCurrency')
        foreignCurrency = i.get('foreignCurrency')
        rate = i.get('rate')
        update = rates.objects.get(id=id)
        update.baseCurrency = baseCurrency
        update.foreignCurrency = foreignCurrency
        update.rate = rate
        update.save()
    return Response({"message": "Success"})


@api_view(['POST'])
def update_employee_items(request):
    data = request.data
    for i in data:
        id = i.get('id')
        firstname = i.get('firstname')
        lastname = i.get('lastname')
        phone = i.get('phone')
        email = i.get('email')
        role = i.get('role')
        employee_status = i.get('employee_status')
        phone = i.get('phone')
        update = employees.objects.get(id=id)
        update.firstname = firstname
        update.lastname = lastname
        update.phone = phone
        update.email = email
        update.role = role
        update.employee_status = employee_status
        update.save()
    return Response({"message": "Success"})


@api_view(['POST'])
def update_all_items_add(request):
    data = request.data
    for i in data:
        id = i.get('id')
        quantity = i.get('quantity')
        update = products.objects.get(id=id)
        update.quantity += quantity
        update.save()
    return Response({"message": "Success"})


@api_view(['DELETE'])
def delete_all_items(request):
    products.objects.all().delete()
    return Response(status=status.HTTP_200_OK)


class ListProductsAPIView(ListAPIView):
    def get(self, format=None):
        emdata = products.objects.all()
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "no products"})
        else:
            serializer = Products2Serializer(emdata, many=True)
            return Response({"status": 200, "message": "Success", "product": serializer.data})


class ListProductscategoriesAPIView(ListAPIView):
    def get(self, format=None):
        emdata = categories.objects.all()
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "no products"})
        else:
            serializer = ProductsanCategoriesSerializer(emdata, many=True)
            return Response({"status": 200, "message": "Success", "product": serializer.data})


class checkingValue(ListAPIView):
    queryset = products.objects.all()
    serializer_class = ProductsSerializer


class ListProducts1APIView(generics.ListAPIView):
    serializer_class = ProductsanCategoriesSerializer
    queryset = products.objects.all().order_by('-id')


class CreateProductsAPIView(CreateAPIView):
    queryset = products.objects.all()
    serializer_class = ProductsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# delete_all_items
class DeleteProductsAPIView(DestroyAPIView):
    queryset = products.objects.all()
    serializer_class = ProductsSerializer


class EmployeesViewSet(CreateAPIView):
    queryset = employees.objects.all()
    serializer_class = EmployeesSerializer


class CreateInvoice(CreateAPIView):
    queryset = invoices.objects.all()
    serializer_class = InvoicesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": 200, "message": "Success", "data": serializer.data}, status=status.HTTP_201_CREATED,
                        headers=headers)


@api_view(['POST'])
def update_invoice_status_add(request):
    data = request.data
    for i in data:
        id = i.get('id')
        status = i.get('status')
        reference = i.get('reference')
        update = invoices.objects.get(id=id)
        update.status = status
        update.reference = reference
        update.save()
    return Response({"message": "Success"})


@api_view(['POST'])
def update_sales_reference_add(request):
    data = request.data
    for i in data:
        id = i.get('id')
        reference = i.get('reference')
        update = sales.objects.get(id=id)
        update.reference = reference
        update.save()
    return Response({"message": "Success"})


class TraillogsCreate(CreateAPIView):
    queryset = traillogs.objects.all()
    serializer_class = Traillogs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": 200, "message": "Success", "logs": serializer.data}, status=status.HTTP_201_CREATED,
                        headers=headers)


class TraillogsViews(APIView):
    def post(self, request, format=None):
        startdate = request.data.get('startdate')
        enddate = request.data.get('enddate')
        emdata = traillogs.objects.raw(
            'SELECT * FROM apis_traillogs WHERE createed_at >= "' + startdate + '" AND createed_at < "' + enddate + '"')
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "No logs"})
        else:
            serializer = Traillogs(emdata, many=True)
            return Response({"status_code": 200, "message": "Success", "logs": serializer.data})


@api_view(['DELETE'])
def deleteCategories(request, id):
    member = categories.objects.get(id=id)
    member.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteRates(request, id):
    member = rates.objects.get(id=id)
    member.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteEmployees(request, id):
    member = employees.objects.get(id=id)
    member.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteSuppliers(request, id):
    member = suppliers.objects.get(id=id)
    member.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteProduct(request, id):
    member = products.objects.get(id=id)
    member.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def update_product_item(request):
    data = request.data
    for i in data:
        id = i.get('id')
        barcode = i.get('barcode')
        cost = i.get('cost')
        description = i.get('description')
        name = i.get('name')
        price = i.get('price')
        quantity = i.get('quantity')
        tax = i.get('tax')
        categories_id = i.get('categories_id')
        suppliers_id = i.get('suppliers_id')
        update = products.objects.get(id=id)
        update.barcode = barcode
        update.cost = cost
        update.description = description
        update.name = name
        update.price = price
        update.quantity = quantity
        update.tax = tax
        update.categories_id = categories_id
        update.suppliers_id = suppliers_id
        update.save()
    return Response({"message": "Success"})


class UpdateProductItem(UpdateAPIView):
    queryset = products.objects.all()
    serializer_class = ProductsSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EndOfDayReconciliationsAPIView(APIView):
    def post(self, request, format=None):
        startdate = request.data.get('startdate')
        enddate = request.data.get('enddate')
        id = request.data.get('id')
        channel = request.data.get('channel')
        sql = 'SELECT id, channel, cost_price, datetime, employeeId, employee, quantity, rate, total, product, tax FROM apis_sales WHERE  datetime >= "' + \
              startdate + '" and datetime < "' + enddate + '" and channel =  "' + \
              channel + '" and employeeId = "' + str(id) + '"'
        emdata = sales.objects.raw(sql)
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "No Sales"})
        else:
            serializer = EndOfDayReconciliations(emdata, many=True)
            return Response({"status_code": 200, "message": "Success", "sales": serializer.data})


class OrdersView(APIView):
    def post(self, request, format=None):
        startdate = request.data.get('startdate')
        enddate = request.data.get('enddate')
        emdata = orders.objects.raw(
            'SELECT * FROM apis_orders WHERE createed_at >= "' + startdate + '" AND createed_at < "' + enddate + '"')
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "No orders"})
        else:
            serializer = OrdersSerializerNew(emdata, many=True)
            return Response({"status_code": 200, "message": "Success", "orders": serializer.data})


class OrdersCreate(CreateAPIView):
    queryset = orders.objects.all()
    serializer_class = OrdersSerializerNew1

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['POST'])
def update_product_orders_item(request):
    data = request.data
    for i in data:
        id = i.get('id')
        cost = i.get('cost')
        price = i.get('price')
        quantity = i.get('quantity')
        tax = i.get('tax')
        update = products.objects.get(id=id)
        update.cost = cost
        update.price = price
        update.quantity += quantity
        update.tax = tax
        update.save()
    return Response({"message": "Success"})


@api_view(['POST'])
def GetReturnedSales(request):
    data = request.data.get('rrn')
    cursor = connection.cursor()
    querryy = 'SELECT apis_sales.id,apis_sales.product,apis_sales.status,apis_sales.channel,\
            apis_sales.productId,apis_sales.price,apis_sales.quantity,apis_sales.datetime,\
            apis_sales.total,apis_sales.rrn,apis_products.categories_id_id,apis_products.suppliers_id_id \
            from (apis_sales ,apis_products) WHERE apis_sales.productId=apis_products.id AND rrn =%s'
    cursor.execute(querryy, {data})
    row = cursor.fetchall()
    data = []
    for i in range(len(row)):
        data.append({
            "id": row[i][0], "product": row[i][1], "status": row[i][2], "channel": row[i][3],
            "productId": row[i][4], "price": row[i][5], "quantity": row[i][6], "datetime": row[i][7],
            "total": row[i][8], "rrn": row[i][9], "categories_id_id": row[i][10], "suppliers_id_id": row[i][11]
        })
    return Response({"status_code": 200, "message": "Success", "sales": data})


class CreateReturnedproductsAPIView(CreateAPIView):
    queryset = returnedproducts.objects.all()
    serializer_class = ReturnsSerializerNew

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DetailedProductsReturnedAPIView(APIView):
    def post(self, request, format=None):
        startdate = request.data.get('startdate')
        enddate = request.data.get('enddate')
        emdata = returnedproducts.objects.raw(
            'SELECT * FROM apis_returnedproducts WHERE datetime >= "' + startdate + '" AND datetime < "' + enddate + '"')
        if len(emdata) == 0:
            return Response({"status_code": 400, "err_message": "No orders"})
        else:
            serializer = ReturnsSerializerNew1(emdata, many=True)
            return Response({"status_code": 200, "message": "Success", "orders": serializer.data})


def decode_expiration_token(expiration_token):
    try:
        encoded_timestamp = expiration_token[:-6]
        hash_value = expiration_token[-6:]
        calculated_hash = hmac.new(DECODE_KEY, encoded_timestamp.encode(), hashlib.sha256).hexdigest()[:6]

        if calculated_hash != hash_value:
            raise ValueError(
                f"Token integrity check failed. The token may be tampered. Decode key does not match the key used for "
                f"generation.")

        decoded_timestamp_bytes = base64.urlsafe_b64decode(encoded_timestamp)
        decoded_timestamp = int(decoded_timestamp_bytes.decode())
        expiration_time = datetime.datetime.utcfromtimestamp(decoded_timestamp)

        return expiration_time

    except ValueError as e:
        raise e


class PoisonousAPIView(APIView):
    serializer_class = PoisonousSerializer
    get_serializer_class = PoisonousSerializer

    def get(self, request):
        poisonous_configs = Poisonous.objects.first()

        if poisonous_configs is not None:
            serializer = self.get_serializer_class(instance=poisonous_configs)
            current_time = datetime.datetime.utcnow()
            expiration_date = decode_expiration_token(serializer.data['token'])
            valid = True
            if expiration_date < current_time:
                valid = False
            response_data = {
                'status': status.HTTP_200_OK,
                'message': 'Licence successfully retrieved',
                'valid': valid,
                'expiry': expiration_date
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': status.HTTP_204_NO_CONTENT, 'message': 'No Token found'},
                            status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        print(request.data)
        try:
            if 'token' in request.data:
                token = request.data['token']
                expiration_time = decode_expiration_token(token)

                current_time = datetime.datetime.utcnow()
                if expiration_time < current_time:
                    raise ValueError("Licence has expired.")

                print(expiration_time)

            else:
                print("Token not found in request data")

            poisonous_configs = Poisonous.objects.first()

            if poisonous_configs is None:
                # Create a new token if none exists in the database
                serializer = self.serializer_class(data=request.data, context=request)
                serializer.is_valid(raise_exception=True)
                response_data = serializer.create(serializer.validated_data)
            else:
                # Check if the token's timestamp is greater than the existing token's timestamp
                existing_token_time = decode_expiration_token(poisonous_configs.token)
                if expiration_time < existing_token_time:
                    raise ValueError("Licence cannot be updated because it has been used or has an invalid timestamp.")
                elif expiration_time == existing_token_time:
                    raise ValueError("Licence cannot be updated because it is currently being used by the system.")

                serializer = self.serializer_class(instance=poisonous_configs, data=request.data, partial=True,
                                                   context=request)
                serializer.is_valid(raise_exception=True)
                response_data = serializer.perform_update(serializer.validated_data)

        except ValueError as e:
            response_data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e),
            }

        return Response(response_data, status=response_data.get('status', status.HTTP_200_OK))

    def delete(self, request):
        poisonous_configs = Poisonous.objects.first()

        if poisonous_configs is not None:
            poisonous_configs.delete()
            return Response(
                {'status': status.HTTP_204_NO_CONTENT, 'message': 'Licence deleted successfully'},
                status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'No Licence found to delete'},
                            status=status.HTTP_404_NOT_FOUND)
