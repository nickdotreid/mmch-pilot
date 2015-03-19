from twilio import twiml
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose

from sms.models import Number

@twilio_view
def gateway(request):
    twilio_request = decompose(request)
    # if number isn't associated with a user - ask them to register first
    try:
        user = Number.objects.get(number=twilio_request.get['From',none]).first().user
    except:
        r = twiml.Response()
        r.message('We dont recognize your number - please register online.')
        return r
    # treat message as question
    r = twiml.Response()
    r.message('Thanks for the SMS message!')
    return r