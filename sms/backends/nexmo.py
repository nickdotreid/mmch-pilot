from sendsms.backends.base import BaseSmsBackend
from libnexmo import Nexmo

from django.conf import settings

API_KEY = settings.NEXMO_API_KEY
API_SECRET = settings.NEXMO_API_SECRET_KEY
nexmo = Nexmo(API_KEY, API_SECRET)

class NexmoBackend(BaseSmsBackend):
    def send_messages(self, messages):
        for message in messages:
            for to in message.to:
                try:
                    nexmo.send_sms(
                        frm = settings.NEXMO_DEFAULT_CALLERID,
                        to=to,
                        text=message.body,
                    )
                except:
                    if not self.fail_silently:
                        raise