from django.urls import path
from school import views

app_name = "school"

urlpatterns = [
    path("register/", views.school_register, name="school_register"),
    path("profile/", views.school_profile, name="school_profile"),
    path("update/", views.school_update, name="school_update"),
    path("grade/", views.grade, name="grade"),
    path("grade/<pk>/delete/", views.grade_delete, name="grade_delete"),
    path("grade/<pk>/update/", views.grade_update, name="grade_update"),
]
