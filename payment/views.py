from django.shortcuts import render, redirect
from school.models import Fee, Grade
from django.db import models
from django.views.decorators.http import require_POST
import requests
import json
from django.urls import reverse
from payment.models import Payment


def transactions(request):
    transactions = request.user.payments.all()

    context = {"transactions": transactions}

    return render(request, "payment/transactions.html", context)


def due_payments(request):
    grade_fee = Grade.get_total_fees(request.user.grade)
    previous_payment_total = request.user.payments.filter(
        status=Payment.Status.SUCCESS
    ).aggregate(grand_total=models.Sum("amount"))
    if previous_payment_total["grand_total"] is None:
        due_fee = grade_fee["grand_total"]
    else:
        due_fee = grade_fee["grand_total"] - previous_payment_total["grand_total"]

    context = {
        "grade_fee": grade_fee["grand_total"],
        "fee_structure": grade_fee["fee_structure_description"],
        "due_fee": due_fee,
    }

    return render(request, "payment/due-payments.html", context)


@require_POST
def payment(request):
    # print("payment", request.POST)
    url = "https://dev.khalti.com/api/v2/epayment/initiate/"

    try:
        new_payment = Payment.objects.create(
            student=request.user, amount=request.POST.get("amount")
        )
    except Exception as e:
        print(e)
        return redirect("payment:due_payments")

    print(new_payment.id, new_payment.name, new_payment.amount, new_payment.student)

    payload = json.dumps(
        {
            "return_url": request.build_absolute_uri(reverse("payment:payment_done")),
            "website_url": request.build_absolute_uri("/"),
            "amount": f"{int(float(new_payment.amount) * 100)}",  # in paisa
            "purchase_order_id": f"{new_payment.id}",
            "purchase_order_name": f"{new_payment.name}",
            "customer_info": {
                "name": f"{request.user.first_name} {request.user.last_name}",
                "email": f"{request.user.email}",
                "phone": f"{request.user.phone_number}",
            },
        }
    )
    headers = {
        "Authorization": "key your_api_key",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return redirect(response.json()["payment_url"])


def payment_done(request):
    print("payment done")
    # return render(request, "payment/payment-done.html")
