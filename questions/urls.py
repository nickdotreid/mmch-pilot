from django.conf.urls import patterns, url

urlpatterns = patterns('questions.views',
	url(r'^(?P<question_id>\d+)','detail', name='questions_detail'),
	url(r'^','list', name='questions_list'),
	)