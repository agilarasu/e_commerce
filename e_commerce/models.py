from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid
class Product(models.Model):
    product_id = models.CharField(max_length=200, unique=False, null=True, blank=True,default="x")
    name = models.CharField(max_length=200,default="x")
    price = models.DecimalField(max_digits=5, decimal_places=2,default=1)
    brand = models.CharField(max_length=200, default='Default Brand')
    description = models.TextField()
    image = models.ImageField(upload_to='static/images/')

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=200, unique=False, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.TextField()
    payment_method = models.CharField(max_length=100)
    coupon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'