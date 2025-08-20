from django.contrib import admin
from payment.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "amount",
        "status",
        "created_at",
        "updated_at",
        "student",
        "initial_khalti_id",
        "khalti_status",
        "khalti_transaction_id",
    ]


admin.site.register(Payment, PaymentAdmin)
