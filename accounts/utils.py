def is_email_valid(email):
    if email is not None and email != "" and "@" not in email and "." not in email:
        return False
    return True


def forgot_password_email(email):
    from django.core.mail import send_mail
    from django.conf import settings
    from .models import OTP

    try:
        new_otp = OTP.generate_otp(email)
    except Exception as e:
        raise Exception(str(e))

    subject = "Password Reset"
    message = f"""
    Use the following OTP to reset your password: {new_otp}
    OR
    follow the link to go to the OTP confirmation page: http://127.0.0.1:8000/accounts/otp-confirmation/
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
