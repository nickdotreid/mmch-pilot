from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from questions.models import Answer, Question, Subscription
from django.contrib.auth.models import User

from random import choice
from string import ascii_lowercase, digits

message_received = Signal(providing_args=[
	'text', #Text of recieved message
	'message', #Response message
	])

@receiver(post_save, sender=Answer)
def answer_alert_asker(sender, **kwargs):
    if not 'created' in kwargs or not kwargs['created']:
        return False
    answer = kwargs['instance']

    if answer.user.id == answer.question.user.id:
    	return False

@receiver(message_received)
def handle_question_forum(sender, text, message, **kwargs):
	if not message.reciever.user:
		return False
	if text.lower() == 'exit':
		# Check if active subscription for user, if so kill it
		subscriptions = Subscription.objects.filter(user=message.reciever.user)
		if subscriptions.exists():
			subscriptions.first().delete()
			message.text = "You left the question."
			message.save()
			return True
		message.text = "You are not subscribed to a question. To post a new question, just text it to this number."
		message.save()
		return True
	subscriptions = Subscription.objects.filter(user=message.reciever.user)
	if subscriptions.exists():
		question = subscriptions.first().question
		answer = Answer(
			text = text,
			user = message.reciever.user,
			question = question,
			)
		answer.save()
		message.text = "Your reply has been saved"
		message.save()
		return True
	question = Question(
		text = text,
		user = message.reciever.user,
		)
	question.save()
	message.text = "You have just posted a question. Any further text messages will be counted as a response. Text EXIT, to leave question."
	message.save()




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
def join_response(sender, text, message, **kwargs):
	if message.reciever.user:
		return False
	if sender.session.get('SET_NAME'):
		# Create new user
		user = User()
		user.username = generate_random_username()
		# Split up name into first/last
		pieces = text.split()
		user.first_name = pieces.pop(0)
		user.last_name = ''.join(pieces)
		user.save()

		message.reciever.user = user
		message.reciever.save()

		message.text = "Your name will be displayed as %s" % (user.get_full_name())
		message.save()
		return True
	if text.lower() == 'join':
		message.text = "You are joining our system. Please enter your name as you would like it displayed."
		message.save()
		sender.session['SET_NAME'] = True

@receiver(message_received)
def default_message_response(sender, text, message, **kwargs):
	if message.text:
		return False
	if message.reciever.user:
		message.text = "We didn't understand your message."
		message.save()
		return True
	message.text = "Welcome to our SMS program, to join, respond with join."
	message.save()