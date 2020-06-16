from django.contrib.auth.models import User
from .models import Employee

def create_user(id):
    try:
        employee = Employee.objects.get(code=id)
    except:
        print("Not found")
    user = User.objects.filter(email = employee.Email)
    if user:
        employee.user_model = user[0]
        employee.save()
    else:
        arroba = employee.Email.find("@")
        user_name = employee.Email[:arroba]
        user = User.objects.create_user(
            username = user_name,
            password = employee.number_doc,
            email = employee.Email
        )
        user.save()
        employee.user_model = user
        employee.save()