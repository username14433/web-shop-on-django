from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Product, BasketProduct, Basket, Customer, User
from .views import AddToBasketView, HelpView, RegistrationView, MainView
from .forms import RegistrationForm


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
        request = factory.get('/basket/')
        request.user = self.user
        response = AddToBasketView.as_view()(request, slug='test')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/basket/')


    def test_help_view(self):
        factory = RequestFactory()
        request = factory.get('/help/')
        request.user = self.user
        response = HelpView.as_view()(request, slug='test')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/help/')

    def test_registration(self):
        factory = RequestFactory()
        request = factory.get('/registration/')
        request.user = self.user
        response = self.user.post('/registration/', {'username': 'hello', 'phone': '456789',
                                                     'email': 'hello@gmail.com', 'password': 'hello',
                                                     'confirm_password': 'hello'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/help/')
        self.assertIn(self.user, Customer.objects.all())

    def test_login(self):
        factory = RequestFactory()
        request = factory.get('/login/')
        request.user = self.user
        response = self.user.post('/login/', {'password': 'hello', 'phone': '456789',
                                                     'email': 'hello@gmail.com',
                                                     'confirm_password': 'hello'})

    def test_delete_from_basket(self):
        self.basket.product.delete(self.basket_product)
        self.assertFalse(self.basket_product in self.basket.products.all())
        self.assertEqual(self.basket.products.count(), 0)

    def test_home(self):
        self.factory = RequestFactory()
        request = self.factory.get('/')
        response = MainView.as_view()(request, slug='test')
        self.assertEqual(response.url, '/')

