from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from .models import Product, BasketProduct
from .utls import BasketMixin, refresh_basket
from .forms import LoginForm


class MainView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = {
            'products': products
        }
        return render(request, 'app/main.html', context)


class ProductView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'app/product.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class BasketView(BasketMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'basket': self.basket
        }
        return render(request, 'app/basket.html', context)


class AddToBasketView(BasketMixin, View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        basket_product, created = BasketProduct.objects.get_or_create(
            user=self.basket.owner,
            product=product,
            cart=self.basket,
            final_price=0)
        # basket_product.final_price = product.price * self.basket.products.quantity

        if created:
            self.basket.products.add(basket_product)
        refresh_basket(self.basket)
        return redirect('/basket/')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)

        context = {'form': form, }
        return render(request, 'app/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')

        context = {'form': form}
        return render(request, 'app/login.html', context)

class ReistrationView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)

        context = {'form': form, }
        return render(request, 'app/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')

        context = {'form': form}
        return render(request, 'app/login.html', context)

class DeleteBasketProductView(View):
    def get(self, *args, **kwargs):
        slug = kwargs.get('slug')
        product = Product.objects.get(slug=slug)
        product.delete()


