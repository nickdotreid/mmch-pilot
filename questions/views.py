from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from questions.models import Question, Answer

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class QuestionForm(forms.Form):

    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_action = reverse(create)

        self.helper.add_input(Submit('submit', 'Ask Question'))

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
            # add message confirming message save
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
        }, context_instance = RequestContext(request))