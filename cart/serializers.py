from rest_framework import serializers
from .models import Cart
from products.models import Product  # Import Product model

class CartSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Ensure valid product ID

    total_price = serializers.ReadOnlyField()  # Read-only computed field

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity', 'total_price', 'added_at']
        read_only_fields = ['user']  # User is set automatically
