from django.db import models


class School(models.Model):
    admin_user = models.OneToOneField(
        "accounts.CustomUser", on_delete=models.CASCADE, related_name="school"
    )

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)

    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    map_location_url = models.URLField(blank=True, null=True)

    principal_name = models.CharField(max_length=255, blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)

    logo = models.ImageField(upload_to="school_logos/", blank=True, null=True)
    banner_image = models.ImageField(upload_to="school_banners/", blank=True, null=True)
    theme_color = models.CharField(max_length=7, blank=True, null=True)  # Hex code

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classes")

    class Meta:
        unique_together = ("name", "school")

    def __str__(self):
        return f"{self.name} | {self.school}"


class Fee(models.Model):
    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # eg. 1,00,00,000.00
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="fees")

    class Meta:
        unique_together = ("name", "grade")

    def __str__(self):
        return f"{self.name} | {self.grade}"
