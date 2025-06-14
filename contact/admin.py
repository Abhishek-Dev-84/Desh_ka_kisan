from django.contrib import admin
from .models import Contact,MyUser,Product,Order
# Register your models here.

admin.site.register(Contact)
admin.site.register(MyUser)
admin.site.register(Product)
admin.site.register(Order)