from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from school.forms import SchoolForm, GradeForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db import IntegrityError
from school.models import Grade
from django.contrib import messages


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
            try:
                saved_grade = form.save()
            except IntegrityError:
                return JsonResponse(
                    {"success": False, "message": "Grade already exists."}
                )
            else:
                saved_grade_dict = {"id": saved_grade.id, "name": saved_grade.name}
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Grade added successfully.",
                        "data": saved_grade_dict,
                    }
                )

    form = GradeForm()
    grades_list = request.user.school.classes.all()

    context = {"form": form, "grades_list": grades_list}

    return render(request, "school/grade-create-form.html", context)


def grade_delete(request, pk):
    try:
        Grade.objects.get(id=pk).delete()
    except Grade.DoesNotExist:
        return JsonResponse({"success": False, "message": "Grade doesn't exist."})
    else:
        return JsonResponse({"success": True, "message": "Grade deleted successfully."})


def grade_update(request, pk):
    try:
        grade = Grade.objects.get(pk=pk)
    except Grade.DoesNotExist:
        messages.error(request, "Grade does not exist")
        return redirect("school:grade")

    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, "Grade updated successfully")
            return redirect("school:grade")

        messages.error(request, "Failed to update grade")
        return redirect("school:grade")

    else:
        form = GradeForm(instance=grade, request=request)
        context = {"form": form}
        return render(request, "school/grade-update-form.html", context)
