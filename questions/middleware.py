import urllib
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.contrib import messages

from questions.models import Subscription

class QuestionsAuthMiddleware(object):

	def process_view(self, request, view_func, view_args, view_kwargs):
		if request.resolver_match.app_name != 'questions':
			return None
		if not request.user.is_authenticated():
			messages.error(request, "You must be logged in to access questions")
			return redirect("%s?%s" % (reverse("login"), urllib.urlencode({
				'next':request.path,
				})))
		return None

def subscribed_questions(request):
		if request.resolver_match.app_name == 'questions' and request.user.is_authenticated():
			subscribed_questions = [subscription.question.id for subscription in Subscription.objects.filter(
	            user = request.user,
	            ).all()]
			return {
				'current_subscription_question_ids':subscribed_questions
			}
		return {}