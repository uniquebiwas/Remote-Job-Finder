from django.core.mail import send_mail
import uuid
def fnc(email):
    token = str(uuid.uuid4())