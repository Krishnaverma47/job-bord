from django.core.mail import send_mail
from django.conf import settings
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


def send_email(user, uid, token):
    print("User", user)
    print("host email user", settings.EMAIL_HOST_USER)
    subject = 'Account verification email.'
    message = f'Please click the link below to confirm your email and activate your account:\n token :{token} \n uid :{uid}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
    print(f"Verification email send to {user.email}")