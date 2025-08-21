from background_task import background
from django.core.mail import send_mail
from django.conf import settings
from payment.models import Payment
import uuid


@background(schedule=3)
def send_payment_notification(payment_id_str, email):  # background task
    payment_id = uuid.UUID(payment_id_str)
    payment = Payment.objects.get(pk=payment_id)
    subject = "Fee Payment Notification"
    message = (
        f"Dear {payment.student.first_name},\n"
        f"Your payment of Rs. {payment.amount} for {payment.name} {'has been initiated' if payment.status == Payment.Status.INITIATED else 'has been completed successfully.'}.\n"
        f"If you have any questions or concerns, please contact us at {settings.DEFAULT_FROM_EMAIL}."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

    print("Email sent successfully to ", email)
