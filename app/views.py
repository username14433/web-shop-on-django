from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from .models import Product, BasketProduct, Customer
from .utils import BasketMixin, refresh_basket, get_basket_product
from .forms import LoginForm, OrderForm, HelpForm, RegistrationForm
from .email import help
import random


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
            final_price=1)

        if created:
            self.basket.products.add(basket_product)
        refresh_basket(self.basket)
        return redirect('/basket/')


class DeleteBasketProductView(BasketMixin, View):
    def get(self, *args, **kwargs):
        basket_product = get_basket_product(self.basket, kwargs)
        self.basket.products.remove(basket_product)
        basket_product.delete()
        refresh_basket(self.basket)
        return redirect('/basket/')


class EditBasketProductQuantity(BasketMixin, View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        basket_product = BasketProduct.objects.get(
            user=self.basket.owner,
            product=product,
            cart=self.basket
        )
        quantity = int(request.POST.get('qty'))
        basket_product.quantity = quantity
        basket_product.final_price = product.price * basket_product.quantity
        basket_product.save()
        refresh_basket(self.basket)
        return redirect('/basket/')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
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


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm(request.POST or None)

        context = {'form': form, }
        return render(request, 'app/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            help.send_email('You are successfully logged in! Welcome to shop Shop!')
            user = authenticate(username=username, password=password)
            # Customer.objects.create(user)
            login(request, user)
            return redirect('/')
        context = {'form': form}
        return render(request, 'app/registration.html', context)


class BuyBasketView(BasketMixin, View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {'basket': self.basket, 'form': form}
        return render(request, 'app/order.html', context)


class OrderView(BasketMixin, View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {'form': form}
        return render(request, 'app/make-order.html', context)

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.basket = self.basket
            new_order.user = self.basket.owner
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.address = form.cleaned_data['address']
            new_order.save()
            self.basket.in_order = True
            self.basket.save()
            new_order.save()
            self.customer.orders.add(new_order)
            help.send_email(f"Hello! Your order successfully completed. The number of order is - {random.randint(1000000, 100000000000)}")
            return redirect('/')
        return redirect('/order/')


class HelpView(BasketMixin, View):
    def get(self, request, *args, **kwargs):
        form = HelpForm(request.POST or None)
        context = {'form': form}
        return render(request, 'app/help.html', context)

    def post(self, request, *args, **kwargs):
        customer_email = self.customer.email
        form = HelpForm(request.POST or None)
        help.send_email(f'Hello {customer_email}. Technical support will reply to you soon')
        print(f"=================\n"
              f"{form.errors}\n"
              f"=================")
        if form.is_valid():

            print(f"=================\n"
                  f"{form.errors}\n"
                  f"=================")
            return redirect('/')
        else:
            return redirect('/')


class SuccessfullyBought(View):
    def get(self, request, *args, **kwargs):
        context = {'template': 'app/order_characteristic.html'}
        return render(request, 'app/order_characteristic.html', context)
