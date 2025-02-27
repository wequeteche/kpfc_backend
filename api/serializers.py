from django.db import transaction
from rest_framework import serializers
from .models import User, Token, Product, Order, OrderItem, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'cat_image'
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
        )
class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "orders",
        )

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
                    "token",
                    "created_at", 
                    "expires_at", 
                    "user_id", 
                    "is_used",
                )
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
                    "name",
                    "price", 
                    "available", 
                    "unit", 
                )

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'name',
            'description', 
            'price',
            'stock',
            'main_image',
            'image_one',
            'image_two',
            'image_three',
        )
        # category = CategorySerializer

    def validate_price(self, value):
        if value <=0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            ) 
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    product_name = serializers.CharField(source='product.name')
    # main_image = serializers.URLField(source='product.main_image')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price')

    class Meta:
        model = OrderItem
        fields = (
            'product_name', 
            # 'main_image',
            'product_price', 
            'quantity',
            'item_subtotal'
            )
    
class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        # orderitem_data = validated_data.pop('items')

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            
            # if orderitem_data is not None:
            #     # Clear existing items (optional, depends on requirements)
            #     instance.items.all().delete()

            #     # Rectreate items with the updated data
            #     for item in orderitem_data:
            #         OrderItem.objects.create(order=instance, **item)
        return instance
    
    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in orderitem_data:
                OrderItem.objects.create(order=order, **item)
        
        return order

    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items',
        )
        extra_kwargs = {
            'user': {'read_only': True}
        }

class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total')
    # user = serializers.StringRelatedField()
    
    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
         
    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price',


        ) 

class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()