from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Question(models.Model):

    text = models.TextField()
    user = models.ForeignKey(User, related_name='questions')
    
    posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

        ordering = ['-posted']

    def __str__(self):
        return "%s by %s" % (self.text, self.user)

class Answer(models.Model):

    text = models.TextField()
    user = models.ForeignKey(User, related_name='answers')
    question = models.ForeignKey(Question, related_name='answers')

    posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

        ordering = ['-posted']

    def __str__(self):
        return "Answer by %s" % (self.user)

class Subscription(models.Model):

    question = models.ForeignKey(Question, related_name='subscriptions')
    user = models.ForeignKey(User, related_name='subscriptions')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        pass
    

@receiver(post_save, sender=Question)
def question_add_subscription(sender, **kwargs):
    question = kwargs['instance']
    Subscription.objects.get_or_create(
        question = question,
        user = question.user,
        )
    