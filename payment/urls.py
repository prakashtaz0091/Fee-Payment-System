from django.urls import path
from payment import views

app_name = "payment"

urlpatterns = [
    path("transactions/", views.transactions, name="transactions"),
    path("due-payments/", views.due_payments, name="due_payments"),
]
