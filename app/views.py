from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from .models import Product, BasketProduct
from .utils import BasketMixin, refresh_basket, get_basket_product
from .forms import LoginForm, OrderForm, HelpForm
from .email import help


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
        print('hello')
        basket = self.basket
        if form.is_valid():
            new_order = form.save()
            new_order.basket = self.basket
            new_order.customer = self.customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.address = form.cleaned_data['address']
            new_order.make_order_date = form.cleaned_data['make_order_date']
            new_order.get_order_date = form.cleaned_data['get_order_date']
            new_order.card_number = form.cleaned_data['card_number']
            print(new_order)
            new_order.save()
            self.basket.in_order = True
            self.basket.save()
            new_order.basket = self.basket
            new_order.save()
            self.customer.orders.add(new_order)
            return redirect('order/')
        return redirect('/')


class HelpView(BasketMixin, View):
    def get(self, request, *args, **kwargs):
        form = HelpForm(request.POST or None)
        context = {'form': form}
        return render(request, 'app/help.html', context)
    def post(self, request, *args, **kwargs):
        customer_email = self.customer.email
        form = HelpForm(request.POST or None)
        if form.is_valid():
            help.send_email(f'hello {customer_email}')
            return redirect('basket/')
# class SuccessfullySentView(View, HelpForm):
#     def get(self, request, *args, **kwargs):
#         context = {'cleaned_data': self.cleaned_data}
#         return render(request, 'app/successfully_sent_help.html', context)