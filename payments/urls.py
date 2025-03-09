from django.urls import path
from .views import StripePaymentView, PaymentStatusView , PayPalPaymentView

urlpatterns = [
    path('stripe/<int:order_id>/', StripePaymentView.as_view(), name='stripe-payment'),
    path('paypal/<int:order_id>/', PayPalPaymentView.as_view(), name='paypal-payment'),
    path('<int:pk>/', PaymentStatusView.as_view(), name='payment-status'),
]
