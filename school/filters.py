import django_filters
from accounts.models import CustomUser


class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = {
            "first_name": ["icontains"],
            "last_name": ["icontains"],
            "address": ["icontains"],
            "email": ["icontains"],
            "phone_number": ["icontains"],
            "grade": ["exact"],
        }
