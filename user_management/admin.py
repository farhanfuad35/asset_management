from django.contrib import admin
from .models import User, Company, Employee
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(User, CustomUserAdmin)
admin.site.register(Company)
admin.site.register(Employee)
