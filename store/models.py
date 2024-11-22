from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _
from .constants import USER_ROLE, PAYMENT_OPTION, ORDER_HISTORY_STATUS, PAYMENT_STATUS, GENDER, ORDER_STATUS

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser): 
    email = models.EmailField(unique=True)
    first_name=models.CharField(max_length=39, null=True)
    last_name=models.CharField(max_length=92, null=True)
    user_role=models.IntegerField(choices=USER_ROLE, null=True) 
    gender=models.IntegerField(null=True, choices=GENDER)
    mobile=models.IntegerField(default=0, null=True)
    address = models.CharField(max_length=255)
    username = None
    profile_pic= models.ImageField(upload_to='profile_pic/', null=True, blank=True)
    city = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    objects=CustomUserManager()


class Products(models.Model): 
    name = models.CharField(max_length=60) 
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10) 
    description = models.CharField( max_length=250, default='', blank=True, null=True) 
    stock=models.PositiveIntegerField(null=True,blank=True)
    image = models.ImageField(upload_to='product_img/', blank=True, null=True)
    quantity = models.IntegerField(default=1) 
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, related_name='wishlists', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItems(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True) 
    customer = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True) 
    required_items = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Order(models.Model):
    product = models.ForeignKey(Products, 
                                on_delete=models.CASCADE, null=True, blank=True) 
    customer = models.ForeignKey(User, 
                                 on_delete=models.CASCADE,null=True, blank=True) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    customer = models.ForeignKey(User, 
                                 on_delete=models.CASCADE,null=True, blank=True) 
    product = models.ForeignKey(Products, 
                                on_delete=models.CASCADE, null=True, blank=True) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_OPTION)
    delivery_charges = models.PositiveBigIntegerField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50,default=False, choices=ORDER_HISTORY_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Coupon(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
