from django.urls import path, include
from . import views
from .views import *
from django.urls import path

app_name = "blog"
urlpatterns = [
    path('', views.index,name='home'),
    path('OurBrunches', views.OurBrunches,name='OurBrunches'),
    path('customerservice', views.customerservice, name='servicePoilcy'),
    path('goods/', good.as_view(),name='good'),
    path("all-products/", AllProductsView.as_view(), name="allproducts"),
    path("cart-<int:pro_id>/", AddToCart.as_view(), name="cart"),
    path("my-cart/", MyCartView.as_view(), name="cart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path('confirmation/', views.confirmations,name='confirmation'),
    path("Register/", CustomerRegistrationView.as_view(), name="customerregistration"),
    path("logout/", CustomerlogoutView.as_view(), name="customerlogout"),
    path("login/", CustomerloginView.as_view(), name="customerlogin"),
    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(), name="customerorderdetail"),
    path("search/", SearchView.as_view(), name="search"),

    # Admin Side pages
    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
    path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
    path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(), name="adminorderdetail"),
    path("admin-all-orders/", AdminOrderListView.as_view(), name="adminorderlist"),
    path("admin-order-<int:pk>-change/", AdminOrderStatuChangeView.as_view(), name="adminorderstatuschange"),
    path("admin-product/list/", AdminProductListView.as_view(), name="adminproductlist"),
    path("admin-product/add/", AdminProductCreateView.as_view(), name="adminproductcreate"),

]
