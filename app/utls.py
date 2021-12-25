from django.views.generic import View
from .models import Customer, Basket
from django.db import models


class BasketMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            customer = Customer.objects.get(user=user)
            if not customer:
                customer = Customer.objects.create(user=user)
            self.customer = customer
            basket = Basket.objects.get(owner=customer)
            if not basket:
                basket = Basket.objects.create(owner=customer)
        else:
            basket = Basket.objects.get(anonymous_user=True)
            if not basket:
                basket = Basket.objects.create(anonymous_user=True)
        self.basket = basket
        return super().dispatch(request, *args, **kwargs)


def refresh_basket(basket):
    basket_data = basket.products.aggregate(models.Sum('final_price'), models.Count('id'))
    basket.final_price = basket_data.get('final_price__sum')
    basket.total_quantity = basket_data.get('id__count')
    basket.save()
