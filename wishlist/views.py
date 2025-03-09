from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Wishlist
from .serializers import WishlistSerializer

# Add product to wishlist
class AddToWishlistView(generics.CreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Assign logged-in user

# View wishlist items
class ViewWishlistView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

# Remove product from wishlist
class RemoveFromWishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        wishlist_item = get_object_or_404(Wishlist, id=pk, user=request.user)
        wishlist_item.delete()
        return Response({"message": "Item removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)
