from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from school.forms import SchoolForm, GradeForm
from django.urls import reverse_lazy


@require_POST
def school_register(request):
    form_data = request.POST
    form = SchoolForm(form_data, request.FILES, request=request)
    if form.is_valid():
        form.save()
        return redirect("school:school_profile")

    return render(request, "app/dashboard.html", {"form": form})


@require_GET
@login_required
def school_profile(request):
    school_admin = request.user
    print(school_admin.profile_pic)
    try:
        school_data = school_admin.school
    except Exception as e:
        print(e)
        return redirect("app:dashboard")

    context = {"admin": school_admin, "school": school_data}
    return render(request, "school/profile.html", context)


@login_required
def school_update(request):
    if request.method == "POST":
        form_data = request.POST
        form = SchoolForm(
            form_data, request.FILES, instance=request.user.school, request=request
        )
        if form.is_valid():
            form.save()
            return redirect("school:school_profile")

    form = SchoolForm(instance=request.user.school, request=request)
    form_submission_url = reverse_lazy("school:school_update")

    context = {"form": form, "form_submission_url": form_submission_url}

    return render(request, "school/update-school-info.html", context)


def grade(request):
    if request.method == "POST":
        form = GradeForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            # return redirect("school:grade")

    form = GradeForm()
    return render(request, "school/grade-form.html", {"form": form})
