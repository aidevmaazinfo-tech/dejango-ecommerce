from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'

    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.CUSTOMER)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)

    def is_customer(self):
        return self.role == self.Roles.CUSTOMER

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"