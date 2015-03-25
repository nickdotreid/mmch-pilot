from django.db import models
from django.contrib.auth.models import User

def user_unicode(self):
    if self.get_full_name():
    	return self.get_full_name()
    if self.email:
    	return self.email
    return  self.username

User.__unicode__ = user_unicode