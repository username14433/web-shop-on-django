from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from Shop.app.models import Category, Product, BasketProduct, Basket, Customer, User
from Shop.app.views import AddToBasketView


class ShopTestCases(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Бытовые товары', slug='goods')
        image = SimpleUploadedFile('image.jpg', content=b'', content_type='image/jpg')
        self.product = Product.objects.create(title='', image=image)
        self.user = User.objects.create(username='testname', password='1234')
        self.customer = Customer.objects.create(user=self.user)
        self.basket = Basket.objects.create(owner=self.customer)
        self.basket_product = BasketProduct.objects.create(
            user=self.user,
            product=self.product,
            cart=self.basket,
        )

    def test_add_to_basket(self):
        self.basket.product.add(self.basket_product)
        self.assertIn(self.basket_product, self.basket.products.all())
        self.assertEqual(self.basket.products.count(), 1)

    def test_add_to_basket_view(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        response = AddToBasketView.as_view()(request, slug='test')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/basket/')



