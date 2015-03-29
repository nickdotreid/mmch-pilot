from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from questions.models import Question, Answer, Subscription
from questions.forms import QuestionForm, AnswerForm

from django.utils.translation import ugettext_lazy as _


def create(request):
    form = QuestionForm()
    if request.POST:
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question(
                text = form.cleaned_data['text'],
                user = request.user,
                )
            question.save()
            messages.success(request, _("Your question has been posted. You will be alerted of each answer."))
            return redirect('/questions/%d' % (question.id)) #hack to make it work
            return redirect(detail, kwargs={
                'question_id':question.id,
                })
    return render_to_response('questions/create.html',{
        'form':form
        }, context_instance = RequestContext(request))

def list(request):
    return render_to_response('questions/list.html',{
        'questions':Question.objects.all(),
        }, context_instance = RequestContext(request))

def list_subscribed(request):
    return render_to_response('questions/list.html',{
        'questions':Question.objects.filter(subscriptions__user=request.user).all(),
        }, context_instance = RequestContext(request))

def list_user_questions(request):
    return render_to_response('questions/list.html',{
        'questions':Question.objects.filter(user=request.user).all(),
        }, context_instance = RequestContext(request))    

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render_to_response('questions/detail.html',{
        'question':question,
        'answers':question.answers.all(),
        'answer_form': AnswerForm(question = question),
        }, context_instance = RequestContext(request))

def delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.user == request.user or request.user.is_staff:
        question.delete()
        messages.success(request, _("Question has been deleted."))
        return redirect(reverse(list))
    messages.error(request, _("You don't have permission to delete this question."))
    if 'HTTP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])
    return redirect(reverse(list))

def answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = AnswerForm(question = question)
    if request.POST:
        form = AnswerForm(request.POST, question = question)
        if form.is_valid():
            answer = Answer(
                text = form.cleaned_data['text'],
                user = request.user,
                question = question,
                )
            answer.save()
            messages.success(request, _("Your answer has been posted."))
            return redirect('/questions/%d' % (question.id)) #hack to make it work
            return redirect(detail, kwargs={
                'question_id':question.id,
                })
    return render_to_response('questions/answer.html',{
        'question':question,
        'form':form,
        }, context_instance = RequestContext(request))


def subscribe(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if question.has_subscriber(request.user):
        messages.error(request, _("You are already subscribed to this question."))
    else:
        subscription = Subscription(
            user = request.user,
            question = question,
            )
        subscription.save()
        messages.success(request, _("You have been subscribed to this question."))
    return redirect(reverse(detail, kwargs={
        'question_id':question.id
        }))

def unsubscribe(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if question.has_subscriber(request.user):
        Subscription.objects.filter(
            user = request.user,
            question = question,
            ).delete()
    messages.success(request, _("You have been unsubscribed from this question."))
    return redirect(reverse(detail, kwargs={
        'question_id':question.id
        }))