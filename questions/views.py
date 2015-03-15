from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext 

from questions.models import Question, Answer

def list(request):
	return render_to_response('questions/list.html',{
		'questions':Question.objects.all(),
		}, context_instance = RequestContext(request))