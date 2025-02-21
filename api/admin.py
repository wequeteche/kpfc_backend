from django.contrib import admin
from api.models import Order, OrderItem, User, Product, Category, Service
from djangoql.admin import DjangoQLSearchMixin

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = [
    'name',
    # 'slug',
    'price',
    'stock',
    'created',
    'updated',
    'description',
    ]
    list_filter = ['stock', 'created', 'updated']
    list_editable = ['price', 'stock', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'unit',
        'available',
    ]
    list_editable = ['price', 'available', 'unit']
    list_filter = ['available']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
       "email",
        ]
    list_filter = ['is_superuser', 'is_staff']

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
# admin.site.register(User)

