import json
from .models import *
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.utils.http import  urlsafe_base64_encode
from django.utils.encoding import force_bytes #force_str #force_text
from . tokens import generateToken
from message_of_life import settings


def send_email(username,email_user,request,user):
    messages.success(request, f'{username}, your account has been successfully created. We have sent you an email.\n You must comfirm in order to activate your account.')

    """
    # send email when account has been created successfully
    subject = "Welcome to AriHook"
    message = "Welcome " + nom + " " + prenom + "\n thank for chosing our website .\n To order login you need to comfirm your email account.\n thanks\n\n\n AriHook"

    from_email = settings.EMAIL_HOST_USER
    to_list = [email_user]
    send_mail(subject, message, from_email, to_list, fail_silently=False)
    """

    # send the confirmation email
    current_site = get_current_site(request)
    email_suject = "confirm your email AriHook Login!"
    messageConfirm = render_to_string("emailConfimation.html", {
        'name': username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generateToken.make_token(user)
    })

    email = EmailMessage(
        email_suject,
        messageConfirm,
        settings.EMAIL_HOST_USER,
        [email_user]
    )

    email.fail_silently = False
    email.send()
    """
    if email.send() :
        email_envoyer = True
    else:
        email_envoyer = False
    return email_envoyer
    """














