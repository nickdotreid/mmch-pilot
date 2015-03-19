from twilio import twiml
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose

from sms.models import Number
from questions.models import Question

@twilio_view
def gateway(request):
    twilio_request = decompose(request)
    # if number isn't associated with a user - ask them to register first
    try:
        user = Number.objects.get(phone_number=twilio_request.get('From',none)).first().user
    except:
        r = twiml.Response()
        r.message('We dont recognize your number - please register online.')
        return r
    question = Question(
        text = twilio_request.get('Body',none),
        user = user,
        )
    question.save()
    r = twiml.Response()
    r.message('Your message has been saved')
    return r