from django.shortcuts import render, redirect
from .forms import SchoolAdminRegisterForm, SchoolAdminLoginForm


def school_admin_register(request):
    if request.method == "POST":
        form = SchoolAdminRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:school_admin_login")

        context = {"form": form}
        return render(request, "accounts/register.html", context)

    form = SchoolAdminRegisterForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def school_admin_login(request):
    form = SchoolAdminLoginForm()

    context = {"form": form}
    return render(request, "accounts/login.html", context)
