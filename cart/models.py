from django.db import models
from demo.models import Product,Address,Payment
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

#cart model
class Cart(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

        # Getting total price
    def get_total(self):
        total = self.item.price*self.quantity
        floatTotal = float("{0:.2f}".format(total))
        return floatTotal

# Order Model
class Ord(models.Model):
    orderItems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    Address = models.ForeignKey(Address,on_delete=models.SET_NULL, blank=True,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True,null=True)


    def __str__(self):
        return self.user.username

    def get_totals(self):
        total = 0
        for order_item in self.orderItems.all():
            total += order_item.get_total()
        return total
    # To Get Total Quantity of items in Order
    def get_quantity(self):
        total = 0
        for order_item in self.orderItems.all():
            total+= order_item.quantity
        return total
