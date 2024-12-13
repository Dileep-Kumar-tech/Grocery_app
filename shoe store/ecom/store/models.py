from django.db import models


# class categories(models.Model):
#     name = models.CharField(max_length=255, unique=True)

#     def __str__(self):
        # return self.name


class profile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def _str_(self):
        return self.username


class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    # categories = models.ForeignKey(categories, on_delete=models.CASCADE)

    def _str_(self):
        return self.name

class Carts(models.Model):
    customer = models.ForeignKey(profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def _str_(self):
        return f"{self.customer.username} - {self.product.name}"
    