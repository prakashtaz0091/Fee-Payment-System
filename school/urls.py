from django.urls import path
from school import views

app_name = "school"

urlpatterns = [
    path("register/", views.school_register, name="school_register"),
]
