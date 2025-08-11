from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from school.forms import SchoolForm


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
        context = {"form": school_res_form}
        return render(request, "app/dashboard.html", context)

    return render(request, "app/dashboard.html")
