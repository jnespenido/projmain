from django.db import models
from django.contrib.auth.models import User

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    specification = models.TextField()
    quantity = models.PositiveIntegerField()
    condition = models.CharField(max_length=50)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.name
