from django.contrib import admin

from .models import (Product, BasketProduct, Basket, Customer, Category)

models = (Product,BasketProduct, Basket, Customer, Category)
for model in models:
    admin.site.register(model)
