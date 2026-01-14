from django.db import models
from organizations.models import Organization

class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()  # in rupees
    max_members = models.IntegerField()
    api_calls_per_month = models.IntegerField()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
