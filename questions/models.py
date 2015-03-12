from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):

    text = models.TextField()
    user = models.ForeignKey(User, related_name='questions')

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return "%s by %s" % (self.text, self.user)

class Answer(models.Model):

    text = models.TextField()
    user = models.ForeignKey(User, related_name='answers')
    question = models.ForeignKey(Question, related_name='answers')

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return "Answer by %s" % (self.user)
    
    