from rest_framework import serializers, status
from apis.models import traillogs, employees, invoices, products, rates, sales, suppliers, categories, orders, \
    returnedproducts, Poisonous, BaseCurrency


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = employees
        fields = "__all__"


class Employees2Serializer(serializers.ModelSerializer):
    class Meta:
        model = employees
        fields = ['id', 'firstname', 'lastname',
                  'phone', 'email', "role", 'status', "username", "employee_status"]


class Employees1Serializer(serializers.ModelSerializer):
    class Meta:
        model = employees
        fields = ['id', 'username', 'email', 'status',
                  'supervisorcode', 'role', 'employee_status']


class Suppliers1SerializerNew(serializers.ModelSerializer):
    class Meta:
        model = suppliers
        fields = ['id', 'suppliers_name',
                  'suppliers_phone', 'suppliers_address']


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = products
        fields = ["id", "barcode", "cost", "description", "name", "price", "quantity",
                  "tax", "categories_id", "suppliers_id", "order_level"]


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = employees
        fields = ('username', 'password')


class Products2Serializer(serializers.ModelSerializer):
    class Meta:
        model = products
        fields = ['id', 'barcode', 'name', 'price', 'quantity',
                  'cost', 'tax']


class Traillogs(serializers.ModelSerializer):
    class Meta:
        model = traillogs
        fields = ['id', 'username', 'user_id', 'item', 'quantity',
                  'action', 'description', 'createed_at']


class ProductsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = products
        fields = ['quantity']


class RatesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = rates
        fields = ('__all__')


class RatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = rates
        fields = ['id', 'currency', 'rate']


class BaseCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseCurrency
        fields = '__all__'


class GetBaseCurrencySerializer(serializers.ModelSerializer):
    base_currency = RatesSerializer()

    class Meta:
        model = BaseCurrency
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = sales
        fields = ('__all__')


class ViewSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = sales
        fields = ('__all__')


class ViewSuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = suppliers
        fields = ('__all__')


class ViewCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = categories
        fields = ('__all__')


##################################################################


class Products222Serializer(serializers.ModelSerializer):
    class Meta:
        model = categories
        fields = "__all__"


class Suppliers222Serializer(serializers.ModelSerializer):
    class Meta:
        model = suppliers
        fields = "__all__"


class ProductsanCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = products
        fields = '__all__'

    categories_id = Products222Serializer(many=False)
    suppliers_id = Suppliers222Serializer(many=False)


class InvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = invoices
        fields = ['id', 'datetime', 'status', 'reference', 'channel',
                  'amount', 'vat', 'currency', 'employeeId']


class EndOfDayReconciliations(serializers.ModelSerializer):
    class Meta:
        model = sales
        fields = ['id', 'channel', 'cost_price', 'datetime', 'employeeId', 'description',
                  'employee', 'quantity', 'price', 'rate', 'total', 'product', 'tax', 'status']


class ProfitabilityAnalysis(serializers.ModelSerializer):
    class Meta:
        model = products
        fields = '__all__'


class OrdersSerializerNew1(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = ["cost", "description", "name", "price", "quantity",
                  "tax", "categories_id", "suppliers_id"]


class OrdersSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = '__all__'

    categories_id = Products222Serializer(many=False)
    suppliers_id = Suppliers222Serializer(many=False)


class SalesReturned(serializers.ModelSerializer):
    class Meta:
        model = sales
        fields = ['datetime', 'channel', 'id', 'cost_price', 'product', 'employee',
                  'price', 'rate', 'rrn', 'quantity', 'total', 'status']


class ReturnsSerializerNew1(serializers.ModelSerializer):
    class Meta:
        model = returnedproducts
        fields = '__all__'

    categories_id = Products222Serializer(many=False)
    suppliers_id = Suppliers222Serializer(many=False)
    sales_id = SalesReturned(many=False)


class ReturnsSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = returnedproducts
        fields = ["id", "quantity", "categories_id", "suppliers_id", "sales_id"]


class PoisonousSerializer(serializers.ModelSerializer):
    class Meta(Poisonous):
        model = Poisonous
        fields = '__all__'

    def create(self, validated_data):
        try:
            document = super().create(validated_data)

            response_data = {
                'status': status.HTTP_201_CREATED,
                'message': 'Licence successfully created',
                'token': document.token
            }

            print(response_data)

            return response_data

        except Exception as e:
            print(e)
            response_data = {
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'Error: {str(e)}',
            }
            return response_data

    def perform_update(self, validated_data):
        try:
            instance = self.instance
            instance.token = validated_data.get('token', instance.token)
            instance.save()

            response_data = {
                'status': status.HTTP_200_OK,
                'message': 'Licence successfully updated',
                'token': instance.token
            }

            print(response_data)

            return response_data

        except Exception as e:
            print(e)
            response_data = {
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'Error: {str(e)}',
            }
            return response_data
