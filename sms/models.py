from django.db import models

from django.contrib.auth.models import User
from django_twilio.models import Caller

# Create your models here.
class Number(Caller):

    user = models.ForeignKey(User, related_name='numbers', blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Number"
        verbose_name_plural = "Numbers"

    def __str__(self):
        pass

class Message(models.Model):

	# Idea is that System messages are NULL
	sender = models.ForeignKey(Number, null=True, blank=True, related_name='messages_from')
	reciever = models.ForeignKey(Number, null=True, blank=True, related_name='messages_to')

	text = models.CharField(max_length=160, blank=True)
	sent = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name= 'Message'
		verbose_name_plural = 'Messages'

	def __str__(self):
		pass