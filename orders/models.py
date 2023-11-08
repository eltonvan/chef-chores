from django.db import models
from home.models import CustomUser, Roles
from django.forms import CharField
from django.urls import reverse


class Location(models.Model):
    name = models.CharField(max_length=150)
    street = models.CharField(max_length=150)
    house_number = models.CharField(max_length=50)
    city = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=150)
    restaurant_id = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="location"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("location_detail", kwargs={"pk": self.pk})


class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    street = models.CharField(max_length=150)
    house_number = models.CharField(max_length=50)
    city = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="restaurant"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("restaurant_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
