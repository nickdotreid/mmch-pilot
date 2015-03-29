# myapp/apps.py
from django.apps import AppConfig


class MyAppConfig(AppConfig):

    name = 'questions'
    verbose_name = 'Questions App'

    def ready(self):
        # import signal handlers
        import questions.signals