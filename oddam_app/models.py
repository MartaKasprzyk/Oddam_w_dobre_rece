from django.contrib.auth.models import User
from django.db import models

TYPES = {
    (1, "fundacja"),
    (2, "organizacja pozarządowa"),
    (3, "zbiórka lokalna"),
}


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return f'{self.name}'


class Institution(models.Model):
    name = models.CharField(max_length=65)
    description = models.TextField()
    type = models.IntegerField(choices=TYPES, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.name}{self.description}{self.type}'


class Donation(models.Model):
    CHOICES = {
        (1, "TAK"),
        (2, "NIE")
    }
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.IntegerField()
    city = models.CharField(max_length=65)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_taken = models.IntegerField(choices=CHOICES, default=2)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

