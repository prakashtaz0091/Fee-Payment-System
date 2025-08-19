from django.shortcuts import render
from school.models import Fee, Grade
from django.db import models


def transactions(request):
    transactions = request.user.payments.all()

    context = {"transactions": transactions}

    return render(request, "payment/transactions.html", context)


def due_payments(request):
    grade_fee = Grade.get_total_fees(request.user.grade)
    previous_payment_total = request.user.payments.aggregate(
        grand_total=models.Sum("amount")
    )
    due_fee = grade_fee["grand_total"] - previous_payment_total["grand_total"]
    context = {
        "grade_fee": grade_fee["grand_total"],
        "fee_structure": grade_fee["fee_structure_description"],
        "due_fee": due_fee,
    }

    return render(request, "payment/due-payments.html", context)
