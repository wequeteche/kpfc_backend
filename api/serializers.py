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
            # 'category_name',
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
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price')

    class Meta:
        model = OrderItem
        fields = (
            'product_name', 
            'product_price', 
            'quantity',
            'item_subtotal'
            )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total')

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