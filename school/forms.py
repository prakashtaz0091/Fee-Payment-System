from django import forms
from school.models import School, Grade, Fee
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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") if "request" in kwargs else None
        super().__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        school = super(SchoolForm, self).save(commit=False, *args, **kwargs)

        if self.request:
            school.admin_user = self.request.user

        if not school.code:
            school_name = self.cleaned_data.get("name")
            school_name_words = school_name.split(" ")
            estd_year = self.cleaned_data.get("established_date").year
            code = "".join([word[0] for word in school_name_words]) + f"-{estd_year}"
            school.code = code
            school.slug = slugify(school_name)

        if commit:
            school.save()

        return school


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") if "request" in kwargs else None
        super().__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        grade = super(GradeForm, self).save(commit=False, *args, **kwargs)
        grade.school = self.request.user.school

        if commit:
            grade.save()

        return grade


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ["name", "amount", "grade"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") if "request" in kwargs else None
        super().__init__(*args, **kwargs)

        if self.request:
            self.fields["grade"].queryset = Grade.objects.filter(
                school__admin_user__id=self.request.user.id
            )
