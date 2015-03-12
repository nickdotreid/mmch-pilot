from django.db import models

from django.contrib.auth.models import User
from django_twilio.models import Caller

# Create your models here.
class Number(Caller):

    user = models.ForeignKey(User, related_name='numbers')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Number"
        verbose_name_plural = "Numbers"

    def __str__(self):
        pass
