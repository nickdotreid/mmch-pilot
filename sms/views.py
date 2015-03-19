from twilio import twiml
from django_twilio.decorators import twilio_view

@twilio_view
def gateway(request):
    r = twiml.Response()
    r.message('Thanks for the SMS message!')
    return r