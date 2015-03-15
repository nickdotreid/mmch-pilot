from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext 

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_action = reverse(login)

        self.helper.add_input(Submit('submit', 'Login'))


# Create your views here.
def home(request):
    return render_to_response('homepage.html',{

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