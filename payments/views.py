import stripe
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Payment
from .serializers import PaymentSerializer
from orders.models import Order
from orders.utils import send_payment_receipt_email
stripe.api_key = settings.STRIPE_SECRET_KEY  # Set Stripe secret key
import paypalrestsdk

# Process payment using Stripe
class StripePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        if Payment.objects.filter(order=order).exists():
            return Response({"error": "Payment for this order already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),  # Convert to cents
                currency="usd",
                payment_method_types=["card"],
            )

            # Save payment details
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=order.total_price,
                payment_method="Stripe",
                transaction_id=intent["id"],
                status="Pending",
            )

            return Response({"client_secret": intent["client_secret"], "payment_id": payment.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# View Payment Status
class PaymentStatusView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

# Process Payment using PayPal without send email
class PayPalPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if Payment.objects.filter(order=order).exists():
            return Response({"error": "Payment for this order already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create PayPal Payment
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": "http://127.0.0.1:8000/api/payments/paypal/success/",
                    "cancel_url": "http://127.0.0.1:8000/api/payments/paypal/cancel/"
                },
                "transactions": [{
                    "amount": {
                        "total": str(order.total_price),
                        "currency": "USD"
                    },
                    "description": f"Order {order.id} payment"
                }]
            })

            if payment.create():
                # Save payment details
                new_payment = Payment.objects.create(
                    user=request.user,
                    order=order,
                    amount=order.total_price,
                    payment_method="PayPal",
                    transaction_id=payment["id"],
                    status="Pending",
                )

                # Get approval URL for redirection
                for link in payment["links"]:
                    if link["rel"] == "approval_url":
                        return Response({"approval_url": link["href"], "payment_id": new_payment.id}, status=status.HTTP_201_CREATED)

            return Response({"error": "PayPal payment creation failed"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

 
# Process Payment using PayPal with send email
# class PayPalPaymentView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, order_id):
#         order = get_object_or_404(Order, id=order_id, user=request.user)

#         if Payment.objects.filter(order=order).exists():
#             return Response({"error": "Payment for this order already exists"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Create PayPal Payment
#             payment = paypalrestsdk.Payment({
#                 "intent": "sale",
#                 "payer": {
#                     "payment_method": "paypal"
#                 },
#                 "redirect_urls": {
#                     "return_url": "http://127.0.0.1:8000/api/payments/paypal/success/",
#                     "cancel_url": "http://127.0.0.1:8000/api/payments/paypal/cancel/"
#                 },
#                 "transactions": [{
#                     "amount": {
#                         "total": str(order.total_price),
#                         "currency": "USD"
#                     },
#                     "description": f"Order {order.id} payment"
#                 }]
#             })

#             if payment.create():
#                 # Save payment details
#                 new_payment = Payment.objects.create(
#                     user=request.user,
#                     order=order,
#                     amount=order.total_price,
#                     payment_method="PayPal",
#                     transaction_id=payment["id"],
#                     status="Pending",
#                 )

#                 # ✅ Send payment receipt email
#                 send_payment_receipt_email(request.user.email, new_payment)

#                 # Get approval URL for redirection
#                 for link in payment["links"]:
#                     if link["rel"] == "approval_url":
#                         return Response({"approval_url": link["href"], "payment_id": new_payment.id}, status=status.HTTP_201_CREATED)

#             return Response({"error": "PayPal payment creation failed"}, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StripePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if Payment.objects.filter(order=order).exists():
            return Response({"error": "Payment for this order already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),  # Convert to cents
                currency="usd",
                payment_method_types=["card"],
            )

            # Save payment details
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=order.total_price,
                payment_method="Stripe",
                transaction_id=intent["id"],
                status="Completed",
            )

            # ✅ Send payment receipt email
            send_payment_receipt_email(request.user.email, payment)

            return Response({"client_secret": intent["client_secret"], "payment_id": payment.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
