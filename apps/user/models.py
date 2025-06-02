from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    wallet_address = models.CharField(max_length=42, unique=True, blank=True, null=True)  # Ethereum-адрес
    email = models.EmailField(unique=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Изменяем related_name
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Изменяем related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username
