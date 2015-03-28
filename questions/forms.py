from django.core.urlresolvers import reverse

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.utils.translation import ugettext_lazy as _


class QuestionForm(forms.Form):

    text = forms.CharField(label=_("Enter a question that you would like answered"), widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('questions_create')

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
            self.helper.form_action = reverse('questions_answer', kwargs={
                'question_id':self.question.id,
                })
        self.helper.add_input(Submit('submit', _('Add an answer')))