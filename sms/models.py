from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from nexmomessage import NexmoMessage

from random import choice
from string import ascii_lowercase, digits

from django.db.models.signals import pre_save
from django.dispatch import receiver, Signal

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
    reciever = models.ForeignKey(Number, null=True, blank=True, related_name='messages_to')

    text = models.CharField(max_length=160, blank=True)
    sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name= 'Message'
        verbose_name_plural = 'Messages'

    def send(self):
        if not self.reciever:
            return False
        if settings.NEXMO_DEBUG:
            print '# MESSAGE TO: %s ## %s' % (self.reciever.phone_number, self.text)
            return True
        sms = NexmoMessage({
            'reqtype': 'json',
            'api_key': settings.NEXMO_API_KEY,
            'api_secret': settings.NEXMO_API_SECRET_KEY,
            'from': settings.NEXMO_DEFAULT_CALLERID,
            'to': self.reciever.phone_number.as_e164,
            'text': self.text,
            })
        sms.set_text_info(self.text) #Why do I do this twice?
        return sms.send_request()

    def __str__(self):
        pass

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

    