# myapp/apps.py
from django.apps import AppConfig


class MyAppConfig(AppConfig):

    name = 'sms'
    verbose_name = 'SMS APP'

    def ready(self):
        # import signal handlers
        import sms.signals