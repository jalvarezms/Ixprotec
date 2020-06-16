from django.contrib import admin
from .models import Employee,AssignedSize
from import_export.admin import ImportExportModelAdmin, ImportExportMixin, ImportMixin
from .resources import EmployeeResource, UserResource
from django.http import HttpResponseRedirect
from django.urls import reverse
from import_export.signals import post_export, post_import
from .utils import create_user
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(Employee)
admin.site.register(AssignedSize)

class EmployeeAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = EmployeeResource

admin.site.unregister(Employee)
admin.site.register(Employee, EmployeeAdmin)

class UserAdmin(ImportMixin, UserAdmin):
    resource_class = UserResource
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)