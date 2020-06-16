from django.db.models.signals import post_save
from notifications.signals import notify
from apps.employees.models import Employee
from apps.assignments.models import EmployeeInspection, EmployeeInspectionDetail


def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='was saved')

post_save.connect(my_handler, sender=EmployeeInspection)