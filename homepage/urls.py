from django.conf.urls import patterns, url

urlpatterns = patterns('homepage.views',
	url(r'^register$','register', name='register'),
	url(r'^login$','login', name='login'),
	url(r'^','home', name='home'),
	)