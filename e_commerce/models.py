from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    brand = models.CharField(max_length=200, default='Default Brand')
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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