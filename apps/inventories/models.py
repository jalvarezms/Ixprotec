from django.db import models

from apps.warehouses.models import Warehouse, Storer
from apps.equipments.models import Equipment,Supply
from apps.requests.models   import EmployeeRequest, DetailRequest

from django.db.models import Sum

# Create your models here.

class Provider(models.Model):
    name = models.CharField(unique=True, max_length = 80 , null=True)
    NIT = models.CharField(unique=True, max_length = 15 , null=True)
    Address = models.CharField(unique=True, max_length = 400 , null=True)
    PhoneNumber = models.CharField(unique=True, max_length = 20 , null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)
    def __str__(self):
        return '%s - %s' % (self.NIT, self.name.upper())

class ReasonMovement(models.Model):
    CODE_ENTRY = 1
    CODE_OUTPUT = 2
    STATUS_CHOICES = [
        (CODE_ENTRY, 'Entry'),
        (CODE_OUTPUT, 'OutPut'),
        ]
    BADGE_CHOICES = [
        (CODE_ENTRY,'badge-info'),
        (CODE_OUTPUT,'badge-warning'),
        ]     
    reason = models.CharField( max_length=50)
    type_movement = models.IntegerField(choices=STATUS_CHOICES)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)
    
    def __str__(self):
        return '(%s) %s' % (self.movement_text(),self.reason)
 
    def movement_text(self):
        return  self.STATUS_CHOICES[self.type_movement-1][1]   
 
    def type_badge(self):
        return  self.BADGE_CHOICES[self.status-1][0]  
        
class CheckEntry(models.Model):
    CODE_PENDING = 1
    CODE_COMPLETED = 2
    STATUS_CHOICES = [
        (CODE_PENDING, 'Pending Entry'),
        (CODE_COMPLETED, 'Completed'),
        ]
    BADGE_CHOICES = [
        (CODE_PENDING,'badge-warning'),
        (CODE_COMPLETED,'badge-success'),
        ]    
    date_entry = models.DateField()
    warehouse  = models.ForeignKey(Warehouse,blank=True, null=True, on_delete=models.SET_NULL)
    bill       = models.CharField(max_length=50)
    provider   = models.ForeignKey(Provider, blank=True,  null=True, on_delete=models.SET_NULL)
    observation = models.TextField(max_length=500)
    storer      = models.ForeignKey(Storer, blank=True, null=True, on_delete=models.SET_NULL)
    reason_movement = models.ForeignKey(ReasonMovement, null=True, blank=True, on_delete=models.SET_NULL)
    status     = models.IntegerField(choices=STATUS_CHOICES,default=CODE_PENDING )
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)

    def __str__(self):
        return '(%s) %s - %s' % (self.warehouse,self.provider, self.bill )

    def total_items(self):
        if self.checkindetail_set.count() > 0 :
           return self.checkindetail_set.aggregate(Sum('total')).get('total__sum')
        else:
            return 0 

    def status_text(self):
        return  self.STATUS_CHOICES[self.status-1][1] 

    def status_badge(self):
        return  self.BADGE_CHOICES[self.status-1][1] 
        

class CheckOutPut(models.Model):
    CODE_PENDING = 1
    CODE_DISPATCHED = 2
    CODE_DELAYED = 3
    CODE_COMPLETED = 4
    STATUS_CHOICES = [
        (CODE_PENDING, 'Pending'),
        (CODE_DISPATCHED, 'Dispached'),
        (CODE_DELAYED, 'Delayed'),
        (CODE_COMPLETED, 'Completed'),
        ]
    BADGE_CHOICES = [
        (CODE_PENDING,'badge-warning'),
        (CODE_DISPATCHED, 'badge-info'),
        (CODE_DELAYED, 'badge-danger'),
        (CODE_COMPLETED,'badge-success'),
        ]
    status     = models.IntegerField(choices=STATUS_CHOICES,default=CODE_PENDING )        
    date_out = models.DateField( null=True)
    warehouse  = models.ForeignKey(Warehouse,blank=True, null=True, on_delete=models.SET_NULL) 
    observation = models.TextField(max_length=500)
    storer      = models.ForeignKey(Storer, blank=True, null=True, on_delete=models.SET_NULL)
    reason_movement = models.ForeignKey(ReasonMovement, null=True, blank=True, on_delete=models.SET_NULL)
    request         = models.ForeignKey(EmployeeRequest, null=True, blank=True, on_delete=models.SET_NULL)
    create_date     = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date   = models.DateTimeField( auto_now=True, blank=True,  null=True)

    def __str__(self):
        return '(%s) %s - %s' % (self.warehouse,self.date_out, self.storer )

    def status_text(self):
        return  self.STATUS_CHOICES[self.status-1][1]    

    def status_badge(self):
        return  self.BADGE_CHOICES[self.status-1][1]

    def get_reason_movement_text(self):
        if self.reason_movement:
            return self.reason_movement.movement_text  
        else:
            return 'OutPut' 
    def get_reason_movement_name(self):
        print("self.reason_movement")
        print(self.reason_movement)
        if self.reason_movement:
            #return 'Pendingxxx'  
            return self.reason_movement.reason  
        else:
            return 'Request pending'             

class CheckOutPutDetail(models.Model):
    STATUS_CHOICES = CheckOutPut.STATUS_CHOICES    
    BADGE_CHOICES  = CheckOutPut.BADGE_CHOICES  

    check_out   =  models.ForeignKey(CheckOutPut, blank=False, null=False, on_delete=models.CASCADE)
    supply  = models.ForeignKey(Supply, null=True, blank=True, on_delete=models.SET_NULL)
    equipment  = models.ForeignKey(Equipment, null=True, blank=True, on_delete=models.SET_NULL)
    total_request = models.IntegerField(default=1)    
    total_dispatched = models.IntegerField(default=1)
    request_detail     = models.ForeignKey(DetailRequest, null=True, blank=True, on_delete=models.SET_NULL)
    status     = models.IntegerField(choices=STATUS_CHOICES,default=CheckOutPut.CODE_PENDING )     
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)

    def status_text(self):
        return  self.STATUS_CHOICES[0][self.status]    

    def status_badge(self):
        return  self.BADGE_CHOICES[0][self.status]

class CheckinDetail(models.Model):
    check_entry = models.ForeignKey(CheckEntry, blank=False, null=False, on_delete=models.CASCADE)
    supply      = models.ForeignKey(Supply, null=True, blank=True, on_delete=models.SET_NULL)
    total       = models.IntegerField()    
    location    = models.CharField( max_length=50)  
    warraty_month = models.IntegerField()
    expire_date  = models.DateField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)


class Movement(models.Model):
    warehouse  = models.ForeignKey(Warehouse,blank=True, null=True, on_delete=models.SET_NULL)
    supply      = models.ForeignKey(Supply, null=True, blank=True, on_delete=models.SET_NULL)
    total       = models.IntegerField()
    post_inventory   = models.IntegerField()
    location    = models.CharField( max_length=50)
    reason_movement = models.ForeignKey(ReasonMovement, null=True, blank=True, on_delete=models.SET_NULL)
    entry_detail = models.ForeignKey(CheckinDetail, blank=True, null=True, on_delete=models.SET_NULL)
    exit_detail   = models.ForeignKey(CheckOutPutDetail, blank=True, null=True, on_delete=models.SET_NULL)
    date_movement = models.DateField( auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)

    def __str__(self):
        return '(%s) %s - %s' % (self.warehouse,self.supply, self.date_movement )

    def identifier(self):
        return '%s%s%s%s%s' % (self.warehouse_id,self.supply_id, self.reason_movement_id,self.create_date.strftime("%y%m%d"),self.id )    

class StockLevel(models.Model):
    warehouse  = models.ForeignKey(Warehouse,blank=True, null=True, on_delete=models.SET_NULL)
    supply      = models.ForeignKey(Supply, null=True, blank=True, on_delete=models.SET_NULL)
    minimum       = models.IntegerField(default=0)
    maximum       = models.IntegerField(default=0)
    stock        = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)  
    
    CODE_UNDEFINED = 1
    CODE_LOW = 2
    CODE_OPTIMUN = 3
    CODE_HIGH = 4
    LEVELS_CHOICES = [
        (CODE_UNDEFINED, 'Undefined!'),
        (CODE_LOW, 'Low!'),
        (CODE_OPTIMUN, 'Optimum!'),
        (CODE_HIGH, 'High'),
        ]
    BADGE_CHOICES = [
        (CODE_UNDEFINED,'badge-warning'),
        (CODE_LOW, 'badge-danger'),
        (CODE_OPTIMUN, 'badge-primary'),
        (CODE_HIGH,'badge-success'),
        ]    

    def get_movement(self):
       return self.supply.movement_set.all()  

    def is_level(self):
        return (True if ( self.minimum != 0 and self.maximum != 0 ) else False)

    def get_level(self):
        if  self.is_level():
            if self.stock <= self.minimum:
                return self.LEVELS_CHOICES[1]
            elif self.stock > self.minimum and self.stock < self.maximum:
                return self.LEVELS_CHOICES[2]
            elif self.stock >= self.maximum:
                return self.LEVELS_CHOICES[3] 
        else:
            return self.LEVELS_CHOICES[0]         

    def get_level_text(self):
        level =  self.get_level()
        return level[1]

    def get_level_id(self):
        level =  self.get_level()
        return level[0]    

    def get_level_badge(self):
        id = self.get_level_id()
        print(id)
        return self.BADGE_CHOICES[id-1][1]    