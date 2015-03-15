from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext 

from questions.models import Question, Answer

def list(request):
	return render_to_response('questions/list.html',{
		'questions':Question.objects.all(),
		}, context_instance = RequestContext(request))

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render_to_response('questions/detail.html',{
		'question':question,
		'answers':question.answers.all(),
		}, context_instance = RequestContext(request))	