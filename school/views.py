from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from school.forms import SchoolForm


@require_POST
def school_register(request):
    form_data = request.POST
    form = SchoolForm(form_data, request.FILES)
    if form.is_valid():
        form.save(request=request)
        return redirect("app:dashboard")

    return render(request, "app/dashboard.html", {"form": form})
