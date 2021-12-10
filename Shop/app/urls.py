from django.urls import path

from .views import (
    MainView,
    ProductView,
    BasketView,
    AddToBasketView,
    LoginView
)

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('products/<str:slug>/', ProductView.as_view(), name='product'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('add-to-basket/<str:slug>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('login/', LoginView.as_view(), name='login')
]
