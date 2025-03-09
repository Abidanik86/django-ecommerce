from django.db import models
from django.conf import settings
from orders.models import Order

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)  # Unique discount code
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Discount in %
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(default=1)  # Max times a coupon can be used
    used_count = models.PositiveIntegerField(default=0)  # Times used

    def is_valid(self):
        """Check if the coupon is valid"""
        from django.utils.timezone import now
        return self.is_active and self.valid_from <= now() <= self.valid_to and self.used_count < self.usage_limit

    def apply_discount(self, total_price):
        """Apply the discount to the total price"""
        return total_price - (total_price * (self.discount_percentage / 100))

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}% Discount"
