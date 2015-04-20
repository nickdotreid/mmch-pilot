from django.conf import settings

from sendsms.backends.base import BaseSmsBackend

kookoo_sms_endpoint = "http://www.kookoo.in/outbound/outbound_sms.php"

'''
This is the library which can be used for sending SMS using Kookoo.
Adopted from:
https://github.com/sidchilling/Kookoo-SMS/blob/master/kookoo_send_sms.py
'''

domain = 'www.kookoo.in'
max_message_length = 150 #Replace this by the length by which you want to restrict the message.
                         #Please note the length is restricted by the telecom provider



class MessageLengthExceededException(Exception):
    '''This exception is raised when the message length is more than the one configured
    '''
    pass

class KookooSendSMSException(Exception):
    '''This exception is raised when the SMS sending encountered an exception from Kookoo
    '''
    def __init__(self, message):
        Exception.__init__(self, message)


def send_kookoo_sms(phone_no = None, message = None):
    '''This method sends a swms using Kookoo. Raises Exception if SMS not successfully sent
    '''
    assert phone_no, 'Phone number cannot be None'
    assert message, 'Message cannot be None'
    if len(message) > max_message_length:
        raise MessageLengthExceededException()
    try:
        import requests
        from xml.dom import minidom
    except:
        print 'Required packages: requests (the one from twitter), xml.doc'
        exit()
    params = {
           'message' : message,
           'phone_no' : phone_no,
           'api_key' : settings.KOOKOO_API_KEY,
        }
    url = kookoo_sms_endpoint
    try:
        response = requests.get(url = url, params = params)
        http_response = minidom.parseString(response.content)
        status = http_response.getElementsByTagName('status')
        if status: # Much pythonic as per PEP 8
            status = status[0]
            if 'success' not in status.toxml():
                raise KookooSendSMSException(http_response.getElementsByTagName('message')[0].toxml())
    except Exception as e:
        print e
        raise Exception(e)

class KooKooSmsBackend(BaseSmsBackend):
    def send_messages(self, messages):
        for message in messages:
            for to in message.to:
                try:
                    send_kookoo_sms(
                        message = message.body,
                        phone_no = to,
                        )
                except:
                    if not self.fail_silently:
                        raise