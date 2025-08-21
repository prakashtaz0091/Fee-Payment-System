from django.shortcuts import render, redirect
from school.models import Fee, Grade
from django.db import models
from django.views.decorators.http import require_POST
import requests
import json
from django.urls import reverse
from payment.models import Payment
from django.contrib import messages
from django.conf import settings
from payment import signals


def transactions(request):
    transactions = request.user.payments.all().order_by("-updated_at")

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
    url = f"{settings.KHALTI_BASE_URL}{settings.KHALTI_INITIATE_URL}"

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
        "Authorization": f"key {settings.KHALTI_SECRET}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return redirect(response.json()["payment_url"])


def payment_done(request):
    # print("payment done")
    query_params = request.GET
    payment_id = query_params.get("purchase_order_id")
    initial_payment_id = query_params.get("pidx")
    status = query_params.get("status")  # if not "Completed" then failed
    amount_in_paisa = int(query_params.get("amount"))
    total_amount_in_paisa = query_params.get("total_amount")
    payment_name = query_params.get("purchase_order_name")
    phone_number = query_params.get("mobile")
    khalti_transaction_id = query_params.get("transaction_id")

    # print("-----------request.GET-------------")
    # print(request.GET)
    # print("-----------request.GET-------------")

    verification_url = f"{settings.KHALTI_BASE_URL}{settings.KHALTI_LOOKUP_URL}"

    payload = json.dumps({"pidx": initial_payment_id})
    headers = {
        "Authorization": f"key {settings.KHALTI_SECRET}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", verification_url, headers=headers, data=payload)

    result = response.json()
    # print("-----------result-------------")
    # print(result)
    # print("-----------result-------------")
    try:
        payment = Payment.objects.get(id=payment_id)  # get the payment object
    except Exception as e:  # if anything wrong happens while getting the payment object
        print(e)
        messages.error(request, "Payment details not found")
        return redirect("payment:due_payments")

    if (  # verification of payment response from khalti with lookup/verification api of khalti
        result["status"] == status
        and result["total_amount"] == amount_in_paisa
        and result["transaction_id"] == khalti_transaction_id
    ):
        if (
            (payment.amount * 100) == result["total_amount"]
        ):  # if amount is not modified by middleman, amount *100, is equal to total_amount
            if result["status"] == "Completed":
                payment.status = Payment.Status.SUCCESS
            elif result["status"] in ("Expired", "Failed", "User canceled"):
                payment.status = Payment.Status.FAILED
            else:
                payment.status = Payment.Status.PENDING

            payment.khalti_status = result["status"]
            payment.khalti_transaction_id = result["transaction_id"]
            payment.initial_khalti_id = result["pidx"]
            payment.save()  # save the payment object with latest khalti details
        else:
            messages.error(request, "Payment amount verification failed")
            return redirect(
                "payment:due_payments"
            )  # redirect to due payments page if payment amount is modified by middleman
    else:
        messages.error(request, "Payment details verification failed")
        payment.status = Payment.Status.FAILED
        payment.save()
        return redirect("payment:due_payments")

    return redirect("payment:transactions")
