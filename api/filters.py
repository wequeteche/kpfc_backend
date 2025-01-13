import django_filters
from api.models import User, Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
                    'name': ['iexact', 'icontains'],
                    'price': ['exact', 'lt', 'gt', 'range'],
                }

# class UserEmailFilter(django_filters.FilterSet):
#     class Meta:
#         model = User
#         fields = ['email']