from django.db.models.signals import post_save
from django.dispatch import receiver
from payment.background_tasks import send_payment_notification


@receiver(post_save, sender="payment.Payment")
def schedule_notification_email(sender, instance, **kwargs):
    send_payment_notification(str(instance.id), instance.student.email)
