from django.db import models
from apps.organizational.models   import Company, Division, Departament, Position
from apps.employees.models    import Employee

# Create your models here.

class Warehouse(models.Model):
    name = models.CharField(max_length=30,null=True, blank=True)
    address = models.TextField(max_length=50,null=True, blank=True)
    phone_number = models.CharField(max_length=15,null=True, blank=True)
    company = models.ForeignKey(to='organizational.Company', null=True, blank=True, on_delete=models.SET_NULL)
    division = models.ForeignKey(Division, null=True, blank=True, on_delete=models.SET_NULL)
    departament = models.ForeignKey(Departament, null=True, blank=True,  on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)    
    modified_date = models.DateTimeField( auto_now=True)
    def __str__(self):
        return '%s' % (self.name)

class Storer(models.Model):
    warehouse = models.ForeignKey(Warehouse, null=True, blank=True,  on_delete=models.SET_NULL)
    position  = models.ForeignKey(Position, null=True, blank=True, on_delete=models.SET_NULL) 
    grand_input = models.BooleanField(default=False)
    grand_output = models.BooleanField(default=False)
    status       = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)    
    modified_date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return '%s' % (self.position)
    





