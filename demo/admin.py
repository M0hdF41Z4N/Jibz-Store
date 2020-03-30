from django.contrib import admin

# Register your models here.
from demo.models import Product,Category,Address,Payment

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(Payment)
