from django.conf import settings
from django.template.loader import render_to_string
from django.template import RequestContext

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver, Signal

from django.utils.translation import ugettext_lazy as _

from questions.models import Answer, Subscription
from django.contrib.auth.models import User

from django.core.mail import send_mail

@receiver(post_save, sender=Answer)
def answer_alert_asker(sender, **kwargs):
    if not 'created' in kwargs or not kwargs['created']:
        return False
    answer = kwargs['instance']

    for subscription in Subscription.objects.filter(question=answer.question).all():
    	if answer.user == subscription.user:
    		continue
    	send_mail(
    		subject = _("A question you are following has been updated"),
    		message = render_to_string( "questions/messages/email_notification.txt",{
    			'answer': answer,
    			'SITE_DOMAIN': settings.SITE_DOMAIN,
    			}), # This is the message
    		from_email = settings.SERVER_EMAIL,
    		recipient_list = [subscription.user.email],
    		fail_silently = False,
    		)