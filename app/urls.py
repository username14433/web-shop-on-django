from django.urls import path
from . import views
from .views import (
    MainView,
    ProductView,
    BasketView,
    AddToBasketView,
    DeleteBasketProductView,
    LoginView,
    EditBasketProductQuantity,
    OrderView,
    BuyBasketView,
    HelpView,

)

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('products/<str:slug>/', ProductView.as_view(), name='product'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('add-to-basket/<str:slug>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('edit-basket-product-quantity/<str:slug>/', EditBasketProductQuantity.as_view(),
         name='edit_basket_product_quantity'),
    path('delete-from-basket/<str:slug>/', DeleteBasketProductView.as_view(), name='delete_from_basket'),
    path('login/', LoginView.as_view(), name='login'),
    path('order/', BuyBasketView.as_view(), name='order'),
    path('make-order/', OrderView.as_view(), name='make_order'),
    path('help/', HelpView.as_view(), name='help'),

    # path('successfully_sent_help', SuccessfullySentView.as_view(), name='successfull_sent')
]
