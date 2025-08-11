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
    latitude = models.DecimalField(
        max_digits=20, decimal_places=13, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=20, decimal_places=13, blank=True, null=True
    )

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
