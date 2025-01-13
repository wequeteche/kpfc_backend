import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class Token(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    user_id = models.IntegerField()
    is_used = models.BooleanField(default=False)

class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(max_length=255)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Service(models.Model):
    name = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True)
    cat_image = models.ImageField(upload_to='category', blank=True, null=True)
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name', 'slug']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    main_image = models.ImageField(upload_to='products', blank=True, null=True)
    image_one = models.ImageField(upload_to='products', blank=True, null=True)
    image_two = models.ImageField(upload_to='products', blank=True, null=True)
    image_three = models.ImageField(upload_to='products', blank=True, null=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
        models.Index(fields=['id']),
        models.Index(fields=['name']),
        models.Index(fields=['-created']),
        ]

    @property
    def in_stock(self):
        return self.stock >0
    def __str__(self):
        return self.name
    
class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    #Never use in production
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    products = models.ManyToManyField(Product, through="OrderItem", related_name='orders')

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        related_name='items'
        )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.order_id}"
    