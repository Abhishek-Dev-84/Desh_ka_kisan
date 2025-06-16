from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.conf import settings
from django.utils import timezone
import uuid
from cloudinary.models import CloudinaryField
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

class MyUserManager(BaseUserManager):
    def create_user(self,username,phone_no,password=None,choice=None):
        if not username:
            raise ValueError("Users must have username")
        user = self.model(username = username,phone_no=phone_no,choice=choice)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,phone_no,password=None,choice=None):
        user = self.create_user(username,phone_no,password,choice)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=25,unique=True)
    phone_no = models.CharField(max_length=10,unique=True)
    choice = models.CharField(max_length=10,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_no','choice']

    def _str_(self):
        return self.username
    
    def has_perm(self,perm,obj=None):
        return self.is_staff or self.is_superuser
    
    def has_module_perms(self,app_label):
        return self.is_superuser
    

ORDER_STATUS_CHOICES = [
    ('pending','Pending'),
    ('out_for_delivery','out for delivery'),
    ('delivered','Delivered'),
    ('cancelled','Cancelled'),
]

class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    category = models.CharField(max_length=15)
    unit = models.CharField(max_length=10,default="kg")
    description = models.TextField()
    image = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    order_id = models.CharField(max_length=100,unique=True,blank=True)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    username = models.CharField(max_length=100,default="unknown")
    full_name = models.CharField(max_length=100,default="unknown")
    mobile = models.CharField(max_length=12,default="unknown")
    house = models.CharField(max_length=255,default="unknown")
    street = models.CharField(max_length=255,default="unknown")
    landmark = models.CharField(max_length=255,blank=True)
    city = models.CharField(max_length=100,default="Unknown")
    state = models.CharField(max_length=100,default="unknown")
    pincode = models.CharField(max_length=10,default="unknown")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=ORDER_STATUS_CHOICES,default= 'pending')
    
    @property
    def total_price(self):
        return self.Product.price*self.quantity
    
    def __str__(self):
        return f"{self.Product.name} - {self.buyer.username}"
    
    def save(self,*args,**kwargs):
        if not self.order_id:
            new_id = generate_order_id()
            while Order.objects.filter(order_id = new_id).exists():
                new_id = generate_order_id()
            self.order_id = new_id
        super().save(*args,**kwargs)

def generate_order_id():
    return 'OD'+ str(uuid.uuid4().hex[:10]).upper()
