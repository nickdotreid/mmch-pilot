from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from questions.models import Answer
from django.contrib.auth.models import User

from random import choice
from string import ascii_lowercase, digits

from django.conf import settings
from twilio.rest import TwilioRestClient

message_received = Signal(providing_args=[
	'text',
	'session',
	])

@receiver(post_save, sender=Answer)
def answer_alert_asker(sender, **kwargs):
    if not 'created' in kwargs or not kwargs['created']:
        return False
    answer = kwargs['instance']

    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=answer.text,
        to= answer.question.user.numbers.first().phone_number.as_e164,
        from_=settings.TWILIO_DEFAULT_CALLERID,
    )

def generate_random_username(length=16, chars=ascii_lowercase+digits, split=4, delimiter='-'):
    username = ''.join([choice(chars) for i in xrange(length)])    
    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])
    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username;

@receiver(message_received)
def set_name_response(sender, text, session, **kwargs):
	if sender.reciever.user:
		return False
	if session.get('SET_NAME'):
		user = User()
		user.username = generate_random_username()
		pieces = text.split()
		user.first_name = pieces.pop(0)
		user.last_name = ''.join(pieces)
		user.save()
		sender.text = "Your name will be displayed as %s" % (user.get_full_name())
		sender.save()
	if text.lower() == 'join':
		sender.text = "You are joining our system. Please enter your name as you would like it displayed."
		sender.save()
		session['SET_NAME'] = True

@receiver(message_received)
def default_message_response(sender, text, session, **kwargs):
	if sender.text:
		return False
	if sender.reciever.user:
		sender.text = "We didn't understand your message."
		sender.save()
		return True
	sender.text = "Welcome to our SMS program, to join, respond with join."
	sender.save()
	return True