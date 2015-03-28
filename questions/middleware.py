import urllib
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.contrib import messages

from questions.models import Subscription
from questions.views import create, list, detail, answer, subscribe, unsubscribe

class QuestionsAuthMiddleware():

	def process_view(self, request, view_func, view_args, view_kwargs):
		if view_func not in [create, list, detail, answer, subscribe, unsubscribe]:
			return None
		if not request.user.is_authenticated():
			messages.error(request, "You must be logged in to do things")
			return redirect("%s?%s" % (reverse("login"), urllib.urlencode({
				'next':request.path,
				})))
		return None

def subscription_processor(request):
    if not 'questions' in request.path or not request.user:
        return {}
    return {
        'current_subscription_question_ids': [subscription.question.id for subscription in Subscription.objects.filter(
            user = request.user,
            ).all()]
    }