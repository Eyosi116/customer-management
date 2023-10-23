from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200 ,null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200 ,null=True)


    def __str__(self):
        return self.name
    


class Product(models.Model):
    CATEGORY = (('Indoor', 'Indoor'), 
                ('Out Door', 'Out Door'),)
    name = models.CharField(max_length=200)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)  # Define the 'category' field with choices
    description = models.CharField(max_length=200, null=True, blank=True) # Define the description field
    date_created = models.DateField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (('Pending', 'Pending'),
              ('Out for delivery', 'Out for delivery'), 
              ('Delivered', 'Delivery'),)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateField(auto_now_add=True, choices=STATUS ,null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.product.name