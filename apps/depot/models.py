__author__ = 'Administrator'
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    description = models.TextField()
    image_url = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=1)
    date_available = models.DateField()

    def __str__(self):
        return self.title


class ProductItem(models.Model):
    product = models.ForeignKey(to=Product)
    unit_price = models.DecimalField(max_digits=8, decimal_places=1)
    quantity = models.IntegerField()


class People(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()

    #class Meta:
    #    abstract = True


class Male(People):
    sex = models.BooleanField()


class Cart(object):
    def __init__(self, items=[], total=0):
        self.items = items
        self.total_price = total

    def add_product(self, product):
        self.total_price += product.price
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += 1
                return
        self.items.append(ProductItem(product=product, unit_price=product.price, quantity=1))


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Restaurant(Place):
    serves_hot_dogs = models.BooleanField()
    serves_pizza = models.BooleanField()


class Supplier(Place):
    customers = models.ManyToManyField(Restaurant)

