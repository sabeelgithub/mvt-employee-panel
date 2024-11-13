from django.db import models
import uuid

from accounts.models import CustomUser

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    custom_fields = models.JSONField(null=True,blank=True)  # Custom fields storage
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    field_order = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name