from django.db import models
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.

#Category Model
class Category(models.Model):
    title = models.CharField(max_length=100)
    primaryCategory = models.BooleanField(default=False)

    def __str__(self):
        return self.title

#Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.SlugField()
    previewText = models.TextField(max_length=100,verbose_name='PreviewText')
    description = models.CharField(max_length=200,verbose_name='Description')
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    #timeStamp = models.DateTimeField()
    thumbnail = models.ImageField(upload_to='products/',default='/products/default.png')

    def __str__(self):
        return self.name

    def get_add_to_cart_url(self):
        return reverse("demo:cart", kwargs = {
        'slug' : self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("demo:remove", kwargs={
        'slug' : self.slug
        })

# Address Model
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    House_no = models.CharField(max_length=100)
    Area = models.CharField(max_length=100)
    Zip = models.IntegerField()
    City = models.CharField(max_length=20)
    State = models.CharField(max_length=20)
    Same_Billing_Address = models.BooleanField()

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount = models.FloatField()
    order_id = models.CharField(max_length=50)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_payment_url(self):
        return reverse("demo:payment",kwargs={
        'slug': self.slug
        })
