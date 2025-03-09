from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from .models import Coupon
from .serializers import CouponSerializer
from orders.models import Order

# Admin: Create Coupon
class CreateCouponView(generics.CreateAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can create coupons

# User: Apply Coupon to Order
class ApplyCouponView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        coupon_code = request.data.get("coupon_code")

        if not coupon_code:
            return Response({"error": "Coupon code is required"}, status=status.HTTP_400_BAD_REQUEST)

        coupon = get_object_or_404(Coupon, code=coupon_code)

        if not coupon.is_valid():
            return Response({"error": "This coupon is expired or has reached its usage limit"}, status=status.HTTP_400_BAD_REQUEST)

        # Apply the discount
        new_total_price = coupon.apply_discount(order.total_price)
        order.total_price = new_total_price
        order.save()

        # Increase coupon usage count
        coupon.used_count += 1
        coupon.save()

        return Response({"message": "Coupon applied successfully", "new_total_price": new_total_price}, status=status.HTTP_200_OK)

# Admin: View All Coupons
class ViewCouponsView(generics.ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can view all coupons

    def get_queryset(self):
        return Coupon.objects.all()
