from django.views.generic import View
from .models import Customer, Basket, BasketProduct, Product
from django.db import models


class BasketMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            customer = Customer.objects.filter(user=user).first()
            if not customer:
                customer = Customer.objects.create(user=user)
            self.customer = customer
            basket = Basket.objects.filter(owner=customer).first()
            if not basket:
                basket = Basket.objects.create(owner=customer)
        else:
            basket = Basket.objects.filter(anonymous_user=True).first()
            if not basket:
                basket = Basket.objects.create(anonymous_user=True)
        self.basket = basket
        return super().dispatch(request, *args, **kwargs)


def refresh_basket(basket):
    basket_data = basket.products.aggregate(models.Sum('final_price'), models.Count('id'))
    basket.final_price = basket_data.get('final_price__sum')
    basket.total_quantity = basket_data.get('id__count')
    basket.save()


def get_basket_product(basket, **kwargs):
    product_slug = kwargs.get('slug')
    product = Product.objects.get(slug=product_slug)
    basket_product = BasketProduct.objects.get(
        user=basket.owner,
        product=product,
        cart=basket
    )
    return basket_product
