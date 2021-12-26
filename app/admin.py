from django.contrib import admin

from .models import (Product, BasketProduct, Basket, Customer, Category, Order)

models = (Product, BasketProduct, Basket, Customer, Category, Order)
for model in models:
    admin.site.register(model)
