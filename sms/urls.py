from django.conf.urls import patterns, url

urlpatterns = patterns('sms.views',
	url(r'^register/(?P<number>.+)','register', name='sms_register'),
	url(r'^register','register', name='sms_register'),
	url(r'^terminal/(?P<number>.+)','terminal', name='sms_terminal'),
	url(r'^terminal','terminal', name='sms_terminal'),
	url(r'^','gateway', name='sms_gateway'),
	)