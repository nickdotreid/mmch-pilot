from django.conf import settings
from django.contrib import messages

from django.utils.translation import ugettext_lazy as _

from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext 

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from sms.models import Number
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

class LoginForm(forms.Form):

    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse(login)

        self.helper.add_input(Submit('submit', _('Login')))

class RegisterForm(forms.Form):
    email = forms.EmailField(label=_("Email"))
    name = forms.CharField(
        label=_("Display name"),
        help_text=_("Enter the name that you would like shown to people on this website. This name doesn't need to be unique, but must be less that 20 characters."),
        max_length=20,
        )
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse(register)

        self.helper.add_input(Submit('submit', _('Register')))


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
    if request.GET.get('next'):
        request.session['next'] = request.GET.get('next')
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
                    if request.session.get('next'):
                        next = request.session.get('next')
                        del request.session['next']
                        return redirect(next)
                    return redirect('/')
                else:
                    messages.error(request, _("Your email address and password did't match"))
            except:
                messages.error(request, _("Your email address wasn't found."))
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
                messages.error(request, _("This email address has already been registered"))
                pass
            else:
                user = User(
                    username = form.cleaned_data['email'],
                    email = form.cleaned_data['email'],
                    )
                user.set_password(form.cleaned_data['password'])

                pieces = form.cleaned_data['name'].split()
                user.first_name = pieces.pop(0)
                user.last_name = ' '.join(pieces)

                user.save()

                user = authenticate(
                    username = form.cleaned_data['email'],
                    password = form.cleaned_data['password'],
                    )
                if user:
                    auth_login(request, user)
                    return redirect(reverse('home'))
        messages.error(request, _("There was an error on your form, please try again."))
    return render_to_response('main/register.html',{
        'form':form,
        }, context_instance = RequestContext(request))