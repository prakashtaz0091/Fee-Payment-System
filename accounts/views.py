from django.shortcuts import render, redirect
from .forms import SchoolAdminRegisterForm, SchoolAdminLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def school_admin_register(request):
    if request.method == "POST":
        form = SchoolAdminRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("accounts:school_admin_login")

        context = {"form": form}
        return render(request, "accounts/register.html", context)

    form = SchoolAdminRegisterForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def school_admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("app:dashboard")

        messages.error(request, "Invalid username or password")
        return redirect("accounts:school_admin_login")

    form = SchoolAdminLoginForm()

    context = {"form": form}
    return render(request, "accounts/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("accounts:school_admin_login")
