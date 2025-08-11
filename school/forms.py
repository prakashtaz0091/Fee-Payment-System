from django import forms
from school.models import School
from django.utils.text import slugify


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = (
            "admin_user",
            "created_at",
            "slug",
            "code",
            "updated_at",
            "is_active",
        )

        widgets = {
            "established_date": forms.DateInput(attrs={"type": "date"}),
            "theme_color": forms.TextInput(attrs={"type": "color"}),
        }

    def save(self, commit=True, request=None, *args, **kwargs):
        school = super(SchoolForm, self).save(commit=False, *args, **kwargs)

        school.admin_user = request.user

        school_name = self.cleaned_data.get("name")
        school_name_words = school_name.split(" ")
        estd_year = self.cleaned_data.get("established_date").year
        code = "".join([word[0] for word in school_name_words]) + f"-{estd_year}"

        school.code = code
        school.slug = slugify(school_name)

        if commit:
            school.save()

        return school
