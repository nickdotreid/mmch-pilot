from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver, Signal

from django.utils.translation import ugettext_lazy as _

from sms.models import Message, RegistrationPin
from questions.models import Answer, Question, Subscription
from django.contrib.auth.models import User

from random import choice
from string import ascii_lowercase, digits

message_received = Signal(providing_args=[
	'message', #Received message
	])

@receiver(post_save, sender=Answer)
def answer_alert_asker(sender, **kwargs):
    if not 'created' in kwargs or not kwargs['created']:
        return False
    answer = kwargs['instance']

    if answer.user.id == answer.question.user.id:
    	return False
    asker = answer.question.user
    
    if not asker.numbers.exists():
    	return False
    message = Message(
    	receiver = asker.numbers.first(),
    	text = "%s: %s" % (answer.user, answer.text),
    	)
    message.save()
    message.send()

@receiver(message_received)
def handle_question_forum(sender, message, **kwargs):
	if not message.sender.user:
		return False
	question_text = _("Confirm that you wanted to post your last message as a question by texting YES.")
	if message.response_to and message.response_to.text == question_text:
		if message.text.lower() == _('yes'):
			question = Question.objects.filter(user = message.sender.user).first()
			question.published = True
			question.save()
			Subscription.objects.get_or_create(
	            question = question,
	            user = message.sender.user,
	            )
			response = Message(
				response_to = message,
				receiver = message.sender,
				text = _('Your question has been published. text EXIT to leave question.'),
				)
			response.save()
			response.send()
			return True
		response = Message(
			response_to = message,
			receiver = message.sender,
			text = _('Your question has not been published.'),
			)
		response.save()
		response.send()
		return True
	# Translators: Word used to exit a conversation
	if message.text.lower() == _('exit'):
		# Check if active subscription for user, if so kill it
		subscriptions = Subscription.objects.filter(user=message.sender.user)
		if subscriptions.exists():
			subscriptions.first().delete()
			response = Message(
				receiver = message.sender,
				text = _("You left the question."),
				response_to = message,
				)
			response.save()
			response.send()
			return True
		response = Message(
			response_to = message,
			receiver = message.sender,
			text = _("You are not subscribed to a question. To post a new question, just text it to this number.")
			)
		response.save()
		response.send()
		return True
	subscriptions = Subscription.objects.filter(user=message.sender.user)
	if subscriptions.exists():
		question = subscriptions.first().question
		answer = Answer(
			text = message.text,
			user = message.sender.user,
			question = question,
			)
		answer.save()
		response = Message(
			response_to = message,
			receiver = message.sender,
			text = _("Your reply has been saved")
			)
		response.save()
		response.send()
		return True
	question = Question(
		text = message.text,
		user = message.sender.user,
		published = False,
		)
	question.save()
	response = Message(
		response_to = message,
		receiver = message.sender,
		text = question_text
		)
	response.save()
	response.send()
	responded = True



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
def join_response(sender, message, **kwargs):
	if message.sender.user:
		return False
	join_text = _("You are joining our system. Please enter your name as you would like it displayed.")
	if message.response_to and message.response_to.text == join_text:
		# Create new user
		user = User()
		user.username = generate_random_username()
		# Split up name into first/last
		pieces = message.text.split()
		user.first_name = pieces.pop(0)
		user.last_name = ' '.join(pieces)
		user.save()

		message.sender.user = user
		message.sender.save()

		response = Message(
			response_to = message,
			receiver = message.sender,
			text = _("Your name will be displayed as %s. You can now post a question by responding to this number.") % (user.get_full_name()),
			)
		response.save()
		response.send()
		return True
	# Translators: Word used to enter webservice
	if message.text.lower() == _('join'):
		response = Message(
			response_to = message,
			receiver = message.sender,
			text = join_text,
			)
		response.save()
		response.send()

@receiver(message_received)
def default_message_response(sender, message, **kwargs):
	if message.responded_to():
		return False
	if message.sender.user:
		response = Message(
			response_to = message,
			receiver = message.sender,
			text = _("We didn't understand your message."),
			)
		response.save()
		response.send()
		responded = True
		return True
	response = Message(
		response_to = message,
		receiver = message.sender,
		text = _("Welcome to our SMS program, to join, respond with join."),
		)
	response.save()
	response.send()