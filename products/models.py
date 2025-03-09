from django.db import models

class Product(models.Model):
    class Categories(models.TextChoices):
        ELECTRONICS = "Electronics", "Electronics"
        FASHION = "Fashion", "Fashion"
        HOME_APPLIANCES = "Home Appliances", "Home Appliances"
        BOOKS = "Books", "Books"
        BEAUTY = "Beauty & Personal Care", "Beauty & Personal Care"

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=50, choices=Categories.choices, default=Categories.ELECTRONICS)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    is_available = models.BooleanField(default=True)  # Changed from is_active

    def __str__(self):
        return self.name
