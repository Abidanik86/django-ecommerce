from django.db import models
from django.conf import settings
from orders.models import Order

class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "Pending", "Pending"
        COMPLETED = "Completed", "Completed"
        FAILED = "Failed", "Failed"
        REFUNDED = "Refunded", "Refunded"

    class PaymentMethod(models.TextChoices):
        STRIPE = "Stripe", "Stripe"
        PAYPAL = "PayPal", "PayPal"
        CASH_ON_DELIVERY = "Cash on Delivery", "Cash on Delivery"
        BANK_TRANSFER = "Bank Transfer", "Bank Transfer"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.STRIPE)
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.order.id} - {self.status}"
