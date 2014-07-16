__author__ = 'Administrator'
from django.test import TestCase
from .forms import ProductForm

class ProductTest(TestCase):
    def setUp(self):
        self.product = {
            'title': 'My Book Title',
            'description': 'yyy',
            'image_url': 'http://google.com/logo.png',
            'price': 1
        }
        f = ProductForm(self.product)
        f.save()
        self.product['title'] = 'My Another Book Title'

    def test_attr_cannot_empty(self):
        f = ProductForm({})
        self.assertFalse(f.is_valid())
        self.assertTrue(f['title'].errors)
        self.assertTrue(f['description'].errors)
        self.assertTrue(f['image_url'].errors)
        self.assertTrue(f['price'].errors)

    def test_price_positice(self):
        for value in [0, -1]:
            self.product['price'] = value
            f = ProductForm(self.product)
            self.assertFalse(f.is_valid())
        self.product['price'] = 1
        f = ProductForm(self.product)
        self.assertTrue(f.is_valid())

    def test_image_url_endwiths(self):
        url_base = 'http://google.com/'
        oks = ('fred.gif', 'fred.jpg', 'fred.png', 'FRED.JPG', 'FRED.Jpg')
        bads = ('fred.doc', 'fred.gif/more', 'fred.gif.more')
        for endwith in oks:
            self.product['image_url'] = url_base + endwith
            f = ProductForm(self.product)
            self.assertTrue(f.is_valid(), msg='error when image_url endwith '+endwith)
        for endwith in bads:
            self.product['image_url'] = url_base + endwith
            f = ProductForm(self.product)
            self.assertFalse(f.is_valid(), msg='error when image_url endwith '+endwith)
        self.product['image_url'] = 'http://google.com/logo.png'

    def test_title_unique(self):
        self.product['title'] = 'My Book Title'
        f = ProductForm(self.product)
        self.assertFalse(f.is_valid())
        self.product['title'] = 'My Another Book Title'