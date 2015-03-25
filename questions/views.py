from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from questions.models import Question, Answer

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.utils.translation import ugettext_lazy as _


class QuestionForm(forms.Form):

    text = forms.CharField(label=_("Enter a question that you would like answered"), widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse(create)

        self.helper.add_input(Submit('submit', _('Ask Question')))

class AnswerForm(forms.Form):
    text = forms.CharField(
        label=_("Enter an answer to the question above"),
        help_text=_('Your answer must be less than 140 characters'),
        widget=forms.Textarea,
        max_length=140,
        )

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', False)
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        if self.question:
            self.helper.form_action = reverse(answer, kwargs={
                'question_id':self.question.id,
                })
        self.helper.add_input(Submit('submit', _('Add an answer')))

@login_required(login_url='login')
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
            messaes.success(request, _("Your question has been posted. You will be alerted of each answer."))
            return redirect('/questions/%d' % (question.id)) #hack to make it work
            return redirect(detail, kwargs={
                'question_id':question.id,
                })
    return render_to_response('questions/create.html',{
        'form':form
        }, context_instance = RequestContext(request))

@login_required(login_url='login')
def list(request):
    return render_to_response('questions/list.html',{
        'questions':Question.objects.all(),
        }, context_instance = RequestContext(request))

@login_required(login_url='login')
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render_to_response('questions/detail.html',{
        'question':question,
        'answers':question.answers.all(),
        'answer_form': AnswerForm(question = question),
        }, context_instance = RequestContext(request))

@login_required(login_url='login')
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
            messages.success(request, _("Your answer has been posted, and we have alerted the original author."))
            return redirect('/questions/%d' % (question.id)) #hack to make it work
            return redirect(detail, kwargs={
                'question_id':question.id,
                })
    return render_to_response('questions/answer.html',{
        'question':question,
        'form':form,
        }, context_instance = RequestContext(request))