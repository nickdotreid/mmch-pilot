from django.conf import settings
import datetime
from django.utils import timezone

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required

from sms.models import Number, Message, RegistrationPin
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
    time = timezone.now() - datetime.timedelta(minutes=5)
    previous_message_query = Message.objects.filter(sent__gte=time, receiver=number)
    if previous_message_query.exists():
        message.response_to = previous_message_query.first()
    message.save()

    responded = False
    message_received.send(
        sender = request,
        message = message,
        )
    return message

def gateway(request):
    # Decode Variables
    if 'msisdn' not in request.GET or 'text' not in request.GET:
        return HttpResponse(status=400)
    handle_message(
        request = request,
        number = '+'+request.GET['msisdn'],
        text = request.GET['text'],
        )
    return HttpResponse(status=200)

def terminal(request, number=None):
    if number:
        numberObj = get_object_or_404(Number, phone_number=number)
        number = numberObj.phone_number.as_e164
    form = TerminalForm(number=number)
    if request.POST:
        form = TerminalForm(request.POST, number=number)
        if form.is_valid():
            numberObj, created = Number.objects.get_or_create(phone_number=form.cleaned_data['phone_number'])
            handle_message(
                request=request,
                number = form.cleaned_data['phone_number'],
                text = form.cleaned_data['message'],
                )
            return redirect(reverse(terminal, kwargs={
                'number':numberObj.phone_number.as_e164,
                }))
    messages = []
    if number:
        messages = Message.objects.filter(
            Q(sender=numberObj) | Q(receiver=numberObj)
            ).all().reverse()
    return render_to_response('sms/terminal.html',{
        'form': form,
        'text_messages':messages,
        }, context_instance=RequestContext(request))


class RegisterForm(forms.Form):
    phone_number = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse(register)
        self.helper.add_input(Submit('submit', 'Add Number'))

@login_required(login_url='login')
def register(request):
    form = RegisterForm()
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            number, created = Number.objects.get_or_create(phone_number=form.cleaned_data['phone_number'])
            pin = RegistrationPin(
                number = number,
                user = request.user,
                ) 
            pin.save()
            message = Message(
                text = "You pin is %s" % (pin.pin),
                receiver = number,
                )
            message.save()
            message.send()
            return redirect(reverse(register_input_pin, kwargs={
                'number': form.cleaned_data['phone_number'],
                }))
    return render_to_response('sms/register.html', {
        'form': form,
        }, context_instance=RequestContext(request))

class InputPinForm(forms.Form):
    pin = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.number = kwargs.pop('number', None)
        super(InputPinForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        if self.number:
            self.helper.form_action = reverse(register_input_pin, kwargs={
                'number':number
                })
        self.helper.add_input(Submit('submit','Enter Pin'))

def register_input_pin(request, number):
    if not request.user.is_authenticated():
        # Push message that login is required
        return redirect("/")
    number = get_object_or_404(Number, phone_number=number)
    form = InputPinForm()
    if request.POST:
        form = InputPinForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data['pin']
            if RegistrationPin.objects.filter(
                pin = pin,
                number = number,
                user = request.user
                ).exists():
                number.user = request.user
                number.save()
                # Add message
                return redirect("/")
    return render_to_response('sms/register.html', {
        'form': form,
        }, context_instance=RequestContext(request))

def list(request):
    messages_list = Message.objects.all()
    paginator = Paginator(messages_list, 25)
    page = request.GET.get('page')

    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        messages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        messages = paginator.page(paginator.num_pages)

    return render_to_response('sms/list.html', {
        "text_messages": messages
        }, context_instance=RequestContext(request))
