import secrets
from django.db import models
from organizations.models import Organization

class APIKey(models.Model):
    key = models.CharField(max_length=64, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = "sk_live_" + secrets.token_hex(20)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.organization.name})"
