from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200, default="")
    contact_no = models.CharField(max_length=20, default="")

    def __str__(self):
        return f"ID: {self.pk} | Name: {self.name} | Address: {self.address} | Contact No. {self.contact_no}"


class User(AbstractUser):
    # Groups
    GROUP_COMAPNY_ADMIN = "COMPANY_ADMIN"
    GROUP_EMPLOYEE = "EMPLOYEE"


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="employee"
    )
    employee_id = models.CharField(
        max_length=80, help_text="Employee ID assigned by the company"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="employees"
    )
    is_company_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_company_admin:
            group_name = self.user.GROUP_COMAPNY_ADMIN
        else:
            group_name = self.user.GROUP_EMPLOYEE

        group = Group.objects.get_or_create(name=group_name)[0]
        self.user.groups.add(group)

    def __str__(self):
        return f"{self.user.first_name}"

    class Meta:
        unique_together = ["employee_id", "company"]
