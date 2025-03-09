from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from cart.models import Cart
from products.models import Product
from .serializers import OrderSerializer
from .utils import send_order_confirmation_email
# Place an order from the cart without send email
class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=user, total_price=total_price)

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            cart_item.delete()  # Clear the cart after order is placed

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

# Place an order from the cart and send email
# class PlaceOrderView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         cart_items = Cart.objects.filter(user=user)

#         if not cart_items.exists():
#             return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

#         total_price = sum(item.product.price * item.quantity for item in cart_items)
#         order = Order.objects.create(user=user, total_price=total_price)

#         for cart_item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=cart_item.product,
#                 quantity=cart_item.quantity,
#                 price=cart_item.product.price
#             )
#             cart_item.delete()  # Clear cart after order is placed

#         # ✅ Send order confirmation email
#         send_order_confirmation_email(user.email, order)

#         return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

# View order history (Authenticated users only)
class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

# Get order details by ID
class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
