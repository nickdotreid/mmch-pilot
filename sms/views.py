from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from twilio import twiml
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose

from sms.models import Number, Message
from questions.models import Question
from django.db.models import Q

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from homepage.views import CustomPhoneNumber

from signals import message_received

class TerminalForm(forms.Form):
    message = forms.CharField()
    phone_number = CustomPhoneNumber()

    def __init__(self, *args, **kwargs):
        self.number = kwargs.pop('number', None)
        super(TerminalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        if self.number:
            self.initial = {
                'phone_number':self.number,
            }
            self.fields['phone_number'].widget = forms.HiddenInput()
            # set and hide phone number input
            self.helper.form_action = reverse(terminal, kwargs={
                'number':self.number,
                })
        self.helper.add_input(Submit('submit', 'Send Message'))

@twilio_view
def gateway(request):
    twilio_request = decompose(request)
    # if number isn't associated with a user - ask them to register first
    print twilio_request.from_
    try:
        user = Number.objects.get(phone_number=twilio_request.from_).user
    except:
        r = twiml.Response()
        r.message('We dont recognize your number: %s' % (twilio_request.from_))
        return r
    question = Question(
        text = twilio_request.body,
        user = user,
        )
    question.save()
    r = twiml.Response()
    r.message('Your message has been saved')
    return r

def terminal(request, number=None):
    if number:
        numberObj = get_object_or_404(Number, phone_number=number)
        number = numberObj.phone_number.as_e164
    form = TerminalForm(number=number)
    if request.POST:
        form = TerminalForm(request.POST, number=number)
        if form.is_valid():
            number, created = Number.objects.get_or_create(
                phone_number=form.cleaned_data['phone_number']
                )
            recieved_message = Message(
                sender = number,
                text = form.cleaned_data['message'],
                )
            recieved_message.save()

            return_message = Message(
                reciever = recieved_message.sender,
                sender = None,
                )
            return_message.save()
            message_received.send(
                sender = return_message,
                text = recieved_message.text,
                session = request.session,
                )
            return redirect(reverse(terminal, kwargs={
                'number':number.phone_number.as_e164,
                }))
    messages = []
    if number:
        messages = Message.objects.filter(
            Q(sender=numberObj) | Q(reciever=numberObj)
            ).all()
    return render_to_response('sms/terminal.html',{
        'form': form,
        'messages':messages,
        }, context_instance=RequestContext(request))