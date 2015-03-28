from django.conf.urls import patterns, url

urlpatterns = patterns('sms.views',
	url(r'^gateway/','gateway', name='sms_gateway'),
	url(r'^register/(?P<number>.+)','register_input_pin', name='sms_input_pin'),
	url(r'^register','register', name='sms_register'),
	url(r'^terminal/(?P<number>.+)','terminal', name='sms_terminal'),
	url(r'^terminal','terminal', name='sms_terminal'),
	)