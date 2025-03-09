from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not phone:
            raise ValueError("The Phone field must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_deleted", False)
        
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone=None, password=None, **extra_fields):
        """Ensuring superuser gets correct permissions"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", CustomUser.UserTypes.SUPERADMIN)

        # Provide a default phone number if not supplied
        if not phone:
            phone = "0000000000"

        return self.create_user(username, email, phone, password, **extra_fields)


class CustomUser(AbstractUser):
    class UserTypes(models.TextChoices):
        SUPERADMIN = "superadmin", "Super Admin"
        ADMIN = "admin", "Admin"
        CUSTOMER = "customer", "Customer"
        SELLER = "seller", "Seller"

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    user_type = models.CharField(
        max_length=20, choices=UserTypes.choices, default=UserTypes.CUSTOMER
    )
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
