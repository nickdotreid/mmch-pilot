from django.conf import settings

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from django_twilio.decorators import twilio_view
from django_twilio.request import decompose

from sms.models import Number, Message
from questions.models import Question
from django.db.models import Q

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from phonenumber_field.formfields import PhoneNumberField as DefaultPhoneNumberField

from signals import message_received

class PhoneNumberField(DefaultPhoneNumberField):

    def to_python(self, value):
        value = ''.join([c for c in value if c in '+1234567890'])
        if '+' not in value:
            try:
                value = settings.DEFAULT_COUNTRY_CODE + value
            except:
                pass
        return super(PhoneNumberField, self).to_python(value)

class TerminalForm(forms.Form):
    message = forms.CharField()
    phone_number = PhoneNumberField()

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

    return return_message.as_twml_response()

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


class RegisterForm(forms.Form):
    phone_number = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse(register)
        self.helper.add_input(Submit('submit', 'Add Number'))

def register(request, number=None):
    if not request.user.is_authenticated():
        # Push message that login is required
        return redirect("/")
    # if number & number exists & pin // show pin screen
    form = RegisterForm()
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            # add pin number
            # send pin to number
            return redirect(reverse(register, kwargs={
                'number': form.cleaned_data['phone_number'],
                }))
    return render_to_response('sms/register.html', {
        'form': form,
        }, context_instance=RequestContext(request))
