from django.db import models

from apps.elements.models import Element_Type,Classification
from apps.employees.models import Employee,AssignedSize
from apps.organizational.models import Position,CostCenter,Location
from apps.equipments.models import Equipment, Color
from datetime import datetime
from django.db.models import Avg, Max, Min, Sum
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class RequestType(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)
    detail = models.TextField(max_length=500)
    status = models.BooleanField(default=False)
    element_type = models.ForeignKey(Element_Type, null=True, blank=True, on_delete=models.SET_NULL)
    element_classification = models.ManyToManyField(Classification, blank=True, related_name='element_class')
    create_date = models.DateTimeField(auto_now_add=True)    
    modified_date = models.DateTimeField( auto_now=True)
    
    def __str__(self):
        return '(%s) %s ' % ( self.code, self.name)

    def status_text(self):
        return {True: 'Activated',False: 'Deactivated'}[self.status]        


# #   Solicitudes de suministros . emcabezado de solicitud antes SuppliesRequest
class EmployeeRequest(models.Model):
    CODE_CREATED = 0
    CODE_APPROVED = 1
    CODE_CANCELED = 2
    CODE_APPROVAL_FLOW = 3
    CODE_DELAYED = 4
    CODE_DECLINED = 5
    CODE_DISPACHED_COMPLETED = 6
    CODE_DISPACHED_INCOMPLETED = 7
    CODE_DELIVERY_RECEIVED = 8
    CODE_APPROVAL_COMPLETED = 9

    STATUS_CHOICES = [
        (CODE_CREATED, _('Created')),
        (CODE_APPROVED, _('Approved')),
        (CODE_CANCELED, _('Canceled')),
        (CODE_APPROVAL_FLOW, _('In Approbal Flow')),
        (CODE_DELAYED, _('Delayed')),
        (CODE_DECLINED, _('Declined')),
        (CODE_DISPACHED_COMPLETED, _('Dispached')),
        (CODE_DISPACHED_INCOMPLETED, _('Incompleted')),
        (CODE_DELIVERY_RECEIVED, _('Received')),
        (CODE_APPROVAL_COMPLETED, _('Approval completed!')),
        ]
    BADGE_CHOICES = [
        (CODE_CREATED,_('badge-warning')),
        (CODE_APPROVED, _('badge-success')),
        (CODE_CANCELED, _('badge-danger')),
        (CODE_APPROVAL_FLOW,_('badge-info')),
        (CODE_DELAYED, _('badge-warning')),
        (CODE_DECLINED, _('badge-danger')),
        (CODE_DISPACHED_COMPLETED, _('badge-success')),
        (CODE_DISPACHED_INCOMPLETED, _('badge-warning')),
        (CODE_DELIVERY_RECEIVED, _('badge-info')),
        (CODE_APPROVAL_COMPLETED, _('badge-success')),
        ]    

    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    request_type = models.ForeignKey(RequestType, null=True, blank=True, on_delete=models.SET_NULL)
    position = models.ForeignKey(Position, null=True, blank=True, on_delete=models.SET_NULL)
    cost_center = models.ForeignKey(CostCenter, null=True, blank=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    code = models.CharField(unique=True, max_length=30)
    observation = models.TextField(max_length=50)
    request_date = models.DateField()
    status_request = models.IntegerField(choices=STATUS_CHOICES, default=CODE_CREATED)
    next_level_approver = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)    
    modified_date = models.DateTimeField( auto_now=True)  

    def __str__(self):
        return '%s - %s ' % ( self.request_type, self.employee)

    def get_employee(self):
        return self.employee

    def request_status(self):
        return self.status_set.all()  

    def status_text(self):        
        return self.STATUS_CHOICES[self.status_request][1]    

    def get_level_badge(self):    
        return self.BADGE_CHOICES[self.status_request][1]

    def get_approver_request_list(self):
        approvers = WorkFlowApprovers.objects.filter( applicant = self.position , request_type=self.request_type ).all()    
        return approvers

    def get_status_list(self):    
        return self.status_set.order_by('-id')

    def get_last_status_activity(self):    
        return self.status_set.latest('id')    

    def get_approver_request(self):
        return WorkFlowApprovers.objects.get( applicant = self.position , request_type=self.request_type ,  level=self.next_level_approver)     

    def get_max_level_work_flow(self):
        level_max = WorkFlowApprovers.objects.filter( applicant = self.position , request_type=self.request_type ).aggregate(Max('level'))
        return level_max
class DetailRequest(models.Model):
    employee_request = models.ForeignKey(EmployeeRequest, null=True, blank=True, on_delete=models.SET_NULL)
    equipment = models.ForeignKey(Equipment, null=True, blank=True, on_delete=models.SET_NULL)
    assigned_size = models.ForeignKey(AssignedSize, null=True, blank=True, on_delete=models.SET_NULL)
    total = models.CharField(max_length=10)
    color = models.ForeignKey(Color,blank=True, null=True,on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)    
    modified_date = models.DateTimeField( auto_now=True)

    def get_employee_request():
        return employee_request

class Status(models.Model):
    CODE_CREATED = 0
    CODE_APPROVED = 1
    CODE_CANCELED = 2
    CODE_APPROVAL_COMPLETED = 3
    CODE_DELAYED = 4
    CODE_DECLINED = 5
    CODE_DISPACHED_COMPLETED = 6
    CODE_DISPACHED_INCOMPLETED = 7
    CODE_RECEIVED_COMPLETED = 8
    CODE_SENDER_APPROVAL_FLOW = 9
    CODE_PENDING_DISPATCH = 10
    CODE_RECEIVED_INCOMPLETED = 11

    STATUS_CHOICES = [
        (CODE_CREATED, _('Created')),
        (CODE_APPROVED, _('Approved')),
        (CODE_CANCELED, _('Canceled')),
        (CODE_APPROVAL_COMPLETED, _('Full Approval')),
        (CODE_DELAYED, _('Delayed')),
        (CODE_DECLINED, _('Declined')),
        (CODE_DISPACHED_COMPLETED, _('Dispatched')),
        (CODE_DISPACHED_INCOMPLETED, _('Incompleted')),
        (CODE_RECEIVED_COMPLETED, _('Received Completed')),
        (CODE_SENDER_APPROVAL_FLOW, _('Sent to Approval')),
        (CODE_PENDING_DISPATCH, _('Pending dispatch')),
        (CODE_RECEIVED_INCOMPLETED, _('Received Incompleted')),
        ]

    BADGE_CHOICES = [
        (CODE_CREATED,_('warning')),
        (CODE_APPROVED, _('success')),
        (CODE_CANCELED, _('danger')),
        (CODE_APPROVAL_COMPLETED, _('success')),
        (CODE_DELAYED, _('warning')),
        (CODE_DECLINED, _('danger')),
        (CODE_DISPACHED_COMPLETED, _('success')),
        (CODE_DISPACHED_INCOMPLETED, _('warning')),
        (CODE_RECEIVED_COMPLETED, _('info')),
        (CODE_SENDER_APPROVAL_FLOW, _('info')),
        (CODE_PENDING_DISPATCH,  _('warning')),
        (CODE_RECEIVED_INCOMPLETED, _('warning')),
        ]     
        
    level = models.IntegerField(default=1)
    date =  models.DateField(default=datetime.now)
    observation = models.TextField(max_length=50)
    status = models.IntegerField(choices=STATUS_CHOICES, default=CODE_CREATED)
    employee_request = models.ForeignKey(EmployeeRequest, null=True, blank=True, on_delete=models.SET_NULL)
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)    
    modified_date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return '(%s-%s) %s' % (self.level, self.STATUS_CHOICES[self.status][1], self.date)

    def status_text(self):        
        return self.STATUS_CHOICES[self.status][1]

    def status_class(self):        
        return self.BADGE_CHOICES[self.status][1]    

class WorkFlowApprovers(models.Model):
    request_type = models.ForeignKey(RequestType, null=True, blank=True, on_delete=models.SET_NULL)
    level = models.IntegerField(default=1)
    applicant = models.ForeignKey(Position,related_name='aplicant_position', null=True, blank=True, on_delete=models.SET_NULL)
    principal_approver = models.ForeignKey(Position,related_name='principal_approver_position', null=True, blank=True, on_delete=models.SET_NULL)
    auxiliar_approver = models.ForeignKey(Position,related_name='auxiliar_approver_position', null=True, blank=True, on_delete=models.SET_NULL)

    create_date = models.DateTimeField(auto_now_add=True)    
    modified_date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return '(%s %s) %s %s' % (self.request_type.code, self.level,self.applicant.code, self.applicant.get_ocupate())