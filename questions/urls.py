from django.conf.urls import patterns, url

urlpatterns = patterns('questions.views',
	url(r'^','list', name='questions_list'),
	)