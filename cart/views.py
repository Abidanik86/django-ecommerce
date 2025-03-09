from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cart
from .serializers import CartSerializer

# Add item to cart
class AddToCartView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]  # User must be logged in

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Assign logged-in user

# View all cart items for logged-in user
class ViewCartView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)  # Show only user's cart

# Update cart item quantity
class UpdateCartView(generics.UpdateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

# Remove item from cart
class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        cart_item = get_object_or_404(Cart, id=pk, user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=204)
