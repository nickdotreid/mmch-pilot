from django.conf.urls import patterns, url

urlpatterns = patterns('questions.views',
	url(r'^(?P<question_id>\d+)/unsubscribe','unsubscribe', name='questions_unsubscribe'),
	url(r'^(?P<question_id>\d+)/subscribe','subscribe', name='questions_subscribe'),
	url(r'^(?P<question_id>\d+)/answer','answer', name='questions_answer'),
	url(r'^(?P<question_id>\d+)/delete','delete', name='questions_delete'),
	url(r'^(?P<question_id>\d+)','detail', name='questions_detail'),
	url(r'^create','create', name='questions_create'),
	url(r'^your','list_user_questions', name='questions_list_user_questions'),
	url(r'^subscribed','list_subscribed', name='questions_list_subscribed'),
	url(r'^','list', name='questions_list'),
	)