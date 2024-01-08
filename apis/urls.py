from django.urls import path
from apis import views
from apis.views import BaseCurrencyView

# allproducts
urlpatterns = [
    path('login/', views.loginViewSet.as_view(), name="login"),
    path('employee/', views.EmployeeManagement.as_view(), name="employee"),
    path('employee/create/', views.EmployeesViewSet.as_view(),
         name="Create Employee"),
    path("view/", views.ListProductsAPIView.as_view(), name="view_product"),
    path("quantity/", views.quantityAPIView.as_view(),
         name="Quantity product"),
    path("viewcategories/", views.ListProductscategoriesAPIView.as_view(),
         name="view_product"),
    path("categories/", views.ViewCategories.as_view(), name="view_categories"),
    path("categories/create/", views.CreateCategories.as_view(),
         name="create_categories/"),
    path("suppliers/", views.ViewSuppliers.as_view(),
         name="view_suppliers"),
    path("outofstock/", views.OutOfStockProducts.as_view(),
         name="create invoice"),
         
    #     delete_all_items DeleteProductsAPIView
    #################################################################

    path("invoice/create/", views.CreateInvoice.as_view(),
         name="create invoice"),

    ###################################################################

    path("suppliers/create/", views.CreateSuppliers.as_view(),
         name="create_suppliers"),
    path("exchangerate/create/", views.CreateExchangeCurrency.as_view(),
         name="Create Exchangerate"),

    path('exchangerate/base-currency/', BaseCurrencyView.as_view(), name='base_currency'),

    path("suppliers/create/", views.CreateSuppliersNew.as_view(),
         name="Create Suppliers"),

    path("views/", views.update_all_items,         name="view_product1"),
    path("update/suppliers/", views.update_suppliers_items,
         name="Update Suppliers"),

    #########################################################

    path("update/invoice/", views.update_invoice_status_add,
         name="Update Invoice"),
    path("update/sales/", views.update_sales_reference_add,
         name="Update Sales"),

    #########################################################

    path("update/employee/", views.update_employee_items,
         name="Update Employee"),
    path("update/exchangerate/", views.update_exchangerate_items,
         name="Update Stock product1"),
    path("add/stock/", views.update_all_items_add, name="Add Stock product1"),
    path("sales/", views.ListSalesAPICreate.as_view(), name="sales"),
    path("view/sales/", views.ListSalesAPIView.as_view(), name="view sales"),
    path("view/teller/sales/", views.EndOfDayReconciliationsAPIView.as_view(),
         name="view sales per teller"),
    path("create/", views.CreateProductsAPIView.as_view(), name="create_product"),
    path("rate/", views.Ratesviews.as_view(), name="rates"),
    path("zwl/rate/", views.RatesviewsZWL.as_view(), name="ZWL rates"),
    path("rate/create/", views.RatesCreateviews.as_view(), name="rate_create"),
    path("update/", views.update_all_items, name="update_product"),
    path("delete/", views.delete_all_items, name="delete_product"),
    path("update/categories/", views.update_categories_items,
         name="Update Categories"),
    path("allproducts/", views.ListProducts1APIView.as_view(), name="rate_create"),

    #################################################################################
    # LOGS
    path("logs/create/", views.TraillogsCreate.as_view(), name="logs_create"),
    path("logs/view/", views.TraillogsViews.as_view(), name="logs_view"),

    #################################################################################

    # DELETE one by one
    path("categories/delete/<int:id>/", views.deleteCategories,
         name="delete_categories"),
    path("rate/delete/<int:id>/", views.deleteRates,
         name="delete_rate"),
    path("employee/delete/<int:id>/", views.deleteEmployees,
         name="delete_rate"),
    path("suppliers/delete/<int:id>/", views.deleteSuppliers,
         name="delete_rate"),
    path("product/delete/<int:id>/", views.deleteProduct,
         name="delete_rate"),

    #################################################################################

    # Update
    path("update/products/", views.update_product_item,
         name="Update Product"),
    path("update/products23/<int:pk>/", views.UpdateProductItem.as_view(),
         name="Update Product"),
    ###############################################################################

    ###########################################################
    # ORDERS APIS

    path("orders/view/", views.OrdersView.as_view(), name="logs_create"),
    path("orders/create/", views.OrdersCreate.as_view(), name="logs_view"),
    path("orders/products/update/", views.update_product_orders_item, name="logs_view"),

    ########################################################### GetReturnedSales

    path("view/returnedsales/", views.GetReturnedSales, name="Get Returned"),
    path("create/returnedsales/", views.CreateReturnedproductsAPIView.as_view(), name="Create Returned Products"),
    path("view/detailed/returned/", views.DetailedProductsReturnedAPIView.as_view(), name="Create Returned Products"),

    ## Poisonous API

    path("poisonous/", views.PoisonousAPIView.as_view(), name="Very Very Poisonous"),
]
