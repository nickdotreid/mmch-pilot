from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext 

# Create your views here.
def home(request):
	return render_to_response('homepage.html',{

		},
		context_instance = RequestContext(request),
		)

def login(request):
	if not request.POST:
		return redirect('/')