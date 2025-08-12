from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from school.forms import SchoolForm
from django.urls import reverse_lazy


@login_required
def dashboard(request):
    try:
        request.user.school
    except Exception as e:
        print(e)
        # message to welcome user and direct them to school registration
        message = (
            "Welcome to the dashboard! Please register your school to get started."
        )
        messages.info(request, message)

        school_res_form = SchoolForm()
        form_submission_url = reverse_lazy("school:school_register")
        context = {"form": school_res_form, "form_submission_url": form_submission_url}
        return render(request, "app/dashboard.html", context)

    return render(request, "app/dashboard.html")
