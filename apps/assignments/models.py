from django.db import models
from apps.employees.models import Employee
from apps.equipments.models import PerPosition, Supply, Equipment, ItemsInspection
from apps.inventories.models import CheckOutPut, CheckOutPutDetail, Movement
from django.contrib.auth.models import User
# Create your models here.

class Delivered(models.Model):
    CODE_PENDING = 1
    CODE_COMPLETED = 2
    CODE_INCOMPLETED = 3

    STATUS_CHOICES = [
        (CODE_PENDING, 'Pending'),
        (CODE_COMPLETED, 'Completed'),
        (CODE_INCOMPLETED, 'Incompleted'),
    ]
    BADGE_CHOICES = [
        (CODE_PENDING,'badge-warning'),
        (CODE_COMPLETED, 'badge-success'),
        (CODE_INCOMPLETED, 'badge-danger'),
    ]
    employee = models.ForeignKey(to='employees.Employee',related_name='delivered_employee', null=True, blank=True, on_delete=models.SET_NULL)
    deliverer = models.ForeignKey(User, related_name='delivered_deliverer', null=True, blank=True, on_delete=models.SET_NULL)
    observation = models.TextField(max_length=250)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)
    checkout = models.ForeignKey(CheckOutPut, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.IntegerField(choices=STATUS_CHOICES, default=CODE_PENDING)
    def __str__(self):
        return '%s' % ( self.employee)
        
    def details(self):
        return self.delivereddetail_set.all()

    def status_text(self):        
        return self.STATUS_CHOICES[self.status-1][1]    

    def get_level_badge(self):    
        return self.BADGE_CHOICES[self.status-1][1]

class DeliveredDetail(models.Model):
    CODE_PENDING = 1
    CODE_ACCEPTED = 2
    CODE_REFUSED = 3

    STATUS_CHOICES = [
        (CODE_PENDING, 'Pending'),
        (CODE_ACCEPTED, 'Accepted'),
        (CODE_REFUSED, 'Refused'),
    ]

    delivered = models.ForeignKey(Delivered, null=True, blank=True, on_delete=models.SET_NULL)        
    observation = models.TextField(max_length=250)
    is_accept   = models.IntegerField(choices=STATUS_CHOICES, default=CODE_PENDING, null=True, blank=True)
    expire_date = models.DateField( blank=True,  null=True)
    supply      = models.ForeignKey(Supply, null=True, blank=True, on_delete=models.SET_NULL) 
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)
    movement = models.ForeignKey(Movement, null=True, blank=True, on_delete=models.SET_NULL)
    checkout_detail = models.ForeignKey(CheckOutPutDetail, null=True, blank=True, on_delete=models.SET_NULL)
#falta campos de movimiento de inventario y salida del almacen
    def __str__(self):
        return '%s %s' % ( self.delivered,self.supply )

    def get_image(self):
        return self.supply.get_photo()

class EmployeeInspection(models.Model):
    BADGE_CHOICES = [
        ('0','badge-danger'),
        ('33','badge-danger'),
        ('66', 'badge-warning'),
        ('99','badge-primary'),
        ]
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    inspection_date = models.DateField(auto_now_add=True)
    observation = models.TextField(max_length=800,default='N/A')
    qualification = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,default=0)

    def inspectioned_elements_count(self):
        return self.employeeinspectiondetail_set.count()

    def get_class_badge_level_average(self):
            if  self.qualification:
                if self.qualification <= 33:
                    return EmployeeInspection.BADGE_CHOICES[1][1]
                elif self.qualification > 33 and self.qualification < 66:
                    return EmployeeInspection.BADGE_CHOICES[2][1]
                elif self.qualification >= 66:
                    return EmployeeInspection.BADGE_CHOICES[3][1]
            else:
                return EmployeeInspection.BADGE_CHOICES[0][1]    

class EmployeeInspectionDetail(models.Model):
    employee_inspection = models.ForeignKey(EmployeeInspection, null=True, blank=True, on_delete=models.SET_NULL)
    delivered_detail = models.ForeignKey(DeliveredDetail, null=True, blank=True, on_delete=models.SET_NULL)
    supply      = models.ForeignKey(Supply, null=True, blank=True, on_delete=models.SET_NULL) 
    equipment = models.ForeignKey(Equipment, null=True, blank=True, on_delete=models.SET_NULL)   

    average = models.DecimalField(max_digits=5, decimal_places=2, blank=True,  null=True,default=0)
    observation = models.TextField(max_length=800,default='N/A')
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)

    def get_class_badge_level_average(self):
            if  self.average:
                if self.average <= 33:
                    return EmployeeInspection.BADGE_CHOICES[1][1]
                elif self.average > 33 and self.average < 66:
                    return EmployeeInspection.BADGE_CHOICES[2][1]
                elif self.average >= 66:
                    return EmployeeInspection.BADGE_CHOICES[3][1]
            else:
                return EmployeeInspection.BADGE_CHOICES[0][1]

class   EmployeeInspectionDetailResponse(models.Model):
    items_inspection = models.ForeignKey(ItemsInspection, null=True, blank=True, on_delete=models.SET_NULL)
    employee_inspection_detail = models.ForeignKey(EmployeeInspectionDetail, null=True, blank=True, on_delete=models.SET_NULL)
    is_positive   = models.BooleanField(default=False)

    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)