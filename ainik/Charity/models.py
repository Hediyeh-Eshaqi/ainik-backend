from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Charity(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(default="")
    description = models.TextField()

class UserCharity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'charity')

class CharityWork(models.Model):
    title = models.CharField(max_length=100)
    type = models.IntegerField()
    charityName = models.ForeignKey(Charity, on_delete=models.CASCADE)
    
