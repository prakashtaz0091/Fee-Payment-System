from django.db import models
import uuid


class Payment(models.Model):
    class Status(models.TextChoices):
        INITIATED = "INITIATED", "Initiated"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    student = models.ForeignKey(
        "accounts.CustomUser", on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    name = models.CharField(max_length=150, blank=True)  # will set in save()

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.INITIATED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:  # only set name if it's not already provided
            # Count how many payments this student has already made in this grade
            previous_count = Payment.objects.filter(student=self.student).count()
            self.name = f"Installment {previous_count + 1}"
        super().save(*args, **kwargs)
