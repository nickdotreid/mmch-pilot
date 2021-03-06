from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from sendsms import api

from random import choice
from string import ascii_lowercase, digits

from django.db.models.signals import pre_save
from django.dispatch import receiver, Signal

from django.utils.encoding import force_unicode

# Create your models here.
class Number(models.Model):

    phone_number = PhoneNumberField()
    active = models.BooleanField(default=True)
    blacklist = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='numbers', blank=True, null=True)

    class Meta:
        verbose_name = "Number"
        verbose_name_plural = "Numbers"

    def __unicode__(self):
        if self.user:
            return unicode(self.user)
        return self.phone_number.as_e164

class Message(models.Model):

    # Idea is that System messages are NULL
    sender = models.ForeignKey(Number, null=True, blank=True, related_name='messages_from')
    receiver = models.ForeignKey(Number, null=True, blank=True, related_name='messages_to')

    text = models.CharField(max_length=160, blank=True)
    sent = models.DateTimeField(auto_now_add=True)

    response_to = models.ForeignKey("Message", null=True, blank=True, related_name='responses')

    class Meta:
        verbose_name= 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-sent','id']

    def send(self):
        if not self.receiver:
            return False
        return api.send_sms(
            body = force_unicode(self.text),
            to = [self.receiver.phone_number.as_e164],
            from_phone = settings.FROM_PHONE_NUMBER,
            )

    def responded_to(self):
        return self.responses.exists()

    def __str__(self):
        if self.sender:
            return "From %s: %s" % (self.sender, self.text)
        if self.receiver:
            return "To %s: %s" % (self.receiver, self.text)
        return self.text

class RegistrationPin(models.Model):

    user = models.ForeignKey(User)
    number = models.ForeignKey(Number)
    pin = models.CharField(max_length=10)
    posted = models.DateTimeField(auto_now_add=True)

    def make_pin(self, length=4, chars=digits):
        pin = ''.join([choice(chars) for i in xrange(length)])
        try:
            RegistrationPin.objects.get(pin=pin)
            return self.make_pin(length=length, chars=chars)
        except RegistrationPin.DoesNotExist:
            return pin;

    class Meta:
        verbose_name = "RegistrationPin"
        verbose_name_plural = "RegistrationPins"

    def __str__(self):
        pass

def set_registration_pin(sender, **kwargs):
    pin = kwargs['instance']
    if not pin.pin:
        pin.pin = pin.make_pin()
pre_save.connect(set_registration_pin, sender=RegistrationPin)

    