from django.contrib import admin



from .models import *


admin.site.register(
    [Customer, Category, goods, Cart, CartProduct,Order,Admin])
