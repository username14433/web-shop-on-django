from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    orders = models.ManyToManyField('Order', related_name='related_custoomer')

    def __str__(self):
        return self.user.first_name, self.user.last_name


class Category(models.Model):
    title = models.CharField('Категория', max_length=45)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField('Товар', max_length=45)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2)
    description = models.CharField(max_length=255)
    image = models.ImageField('Изображение')

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})


class Basket(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField('BasketProduct', related_name='related_cart')
    final_price = models.DecimalField('Финальная цена корзина', max_digits=9, decimal_places=2, null=True)
    total_quantity = models.PositiveIntegerField(default=1)
    in_order = models.BooleanField(default=False)
    anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class BasketProduct(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Basket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество товара в корзине', default=1)
    final_price = models.DecimalField('Финальная цена товара', max_digits=9, decimal_places=2, null=True)
    def __str__(self):
        return f'Продукт {self.product.title}'


class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='related_orders')
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(40, max_length=40)
    address = models.CharField(65, max_length=65)
    make_order_date = models.DateTimeField(10)
    get_order_date = models.DateTimeField(10)
