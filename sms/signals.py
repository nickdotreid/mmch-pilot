from django.db.models.signals import post_save
from django.dispatch import receiver
from questions.models import Answer

from django.conf import settings
from twilio.rest import TwilioRestClient

@receiver(post_save, sender=Answer)
def answer_alert_asker(sender, **kwargs):
    if not 'created' in kwargs or not kwargs['created']:
        return False
    answer = kwargs['instance']

    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=answer.text,
        to= answer.user.numbers.first().phone_number.as_e164,
        from_=settings.TWILIO_DEFAULT_CALLERID,
    )