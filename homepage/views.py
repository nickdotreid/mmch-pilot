from django.conf import settings

from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext 

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from phonenumber_field.formfields import PhoneNumberField

from sms.models import Number
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

class CustomPhoneNumber(PhoneNumberField):

    def to_python(self, value):
        value = ''.join([c for c in value if c in '+1234567890'])
        if '+' not in value:
            try:
                value = settings.DEFAULT_COUNTRY_CODE + value
            except:
                pass
        print "####### Number is %s  #######" % (value)
        return super(PhoneNumberField, self).to_python(value)

class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse(login)

        self.helper.add_input(Submit('submit', 'Login'))

class RegisterForm(forms.Form):
    email = forms.EmailField()
    phone_number = CustomPhoneNumber()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse(register)

        self.helper.add_input(Submit('submit', 'Register'))


# Create your views here.
def home(request):
    if request.user.is_authenticated():
        return redirect(reverse('questions_list'))
    return render_to_response('homepage.html',{
        'login_form':LoginForm(),
        'register_form':RegisterForm(),
        },
        context_instance = RequestContext(request),
        )

def login(request):
    form = LoginForm()
    if request.POST:
        form = LoginForm(request.POST)
        if(form.is_valid()):
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(
                    username = user.username,
                    password = password
                    )
                if user is not None:
                    auth_login(request, user)
                    return redirect('/')
            except:
                pass
    return render_to_response('main/login.html',{
        'form':form,
        }, context_instance = RequestContext(request))

def logout(request):
    auth_logout(request)
    return redirect('/')

def register(request):
    form = RegisterForm()
    if request.POST:
        form = RegisterForm(request.POST)
        if(form.is_valid()):
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                # Set message saying email exists
                pass
            elif Number.objects.filter(phone_number=form.cleaned_data['phone_number']).exists():
                # Set message saying phone number exists
                pass
            else:
                user = User(
                    username = form.cleaned_data['email'],
                    email = form.cleaned_data['email'],
                    )
                user.set_password(form.cleaned_data['password'])
                user.save()

                number = Number(
                    phone_number = form.cleaned_data['phone_number'],
                    user = user,
                    )
                number.save()
                user = authenticate(
                    username = form.cleaned_data['email'],
                    password = form.cleaned_data['password'],
                    )
                if user:
                    auth_login(request, user)
                    return redirect(reverse('home'))
                # add message that something went wrong
    return render_to_response('main/register.html',{
        'form':form,
        }, context_instance = RequestContext(request))