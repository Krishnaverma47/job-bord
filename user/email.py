from django.core.mail import send_mail
from django.conf import settings
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def send_email(email):
    user = User.objects.filter(email=email).first()
    if user:
        print("User", user)
        print("host email user", settings.EMAIL_HOST_USER)
        refresh = RefreshToken.for_user(user)
        subject = "Account verification email."
        message = f"Please click on below link to verify account.\n http://127.0.0.0/8000/{refresh}"
        send_mail(subject,message, settings.EMAIL_HOST_USER, [email])
        print(f"Verification email send to {email}")
    else:
        return {"data":"You are a registered user."}

