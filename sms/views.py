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

def handle_message(request, number, text):
    number, created = Number.objects.get_or_create(phone_number=number)

    message = Message(
        sender = number,
        text = text,
        )
    message.save()

    return_message = Message(
        reciever = message.sender,
        sender = None,
        )
    return_message.save()
    message_received.send(
        sender = request,
        text = message.text,
        message = return_message,
        )
    return return_message

@twilio_view
def gateway(request):
    twilio_request = decompose(request)
    
    return_message = handle_message(
        request=request,
        number = twilio_request.from_,
        text = twilio_request.body,
        )

    r = twiml.Response()
    r.message(return_message.text)
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
                phone_number=form.cleaned_data['phone_number'],
                )
            handle_message(
                request=request,
                number = form.cleaned_data['phone_number'],
                text = form.cleaned_data['message'],
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