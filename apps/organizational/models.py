from django.db import models
from apps.employees.models import Employee
from apps.equipments.models import PerPosition
from datetime import datetime

# Create your models here.
class Company(models.Model):
    code = models.CharField(unique=True, max_length=4)
    name = models.CharField(max_length=30)
    status = models.BooleanField(default=True)
    start_date = models.DateField(null=False, blank=False)
    country_code = models.CharField(max_length=3)
    country_name = models.CharField(max_length=30, default='')
    city_name = models.CharField(max_length=30, default='')
    logo =  models.ImageField(upload_to='uploads/company/logo/', null=True, blank=True, verbose_name='logo')
    telephone =  models.CharField(max_length=15, default='')
    address  = models.CharField(max_length=400, default='N/A')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '(%s) %s' % ( self.code, self.name)


class Division(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=30)
    status = models.BooleanField(default=True)
    start_date = models.DateField(null=False, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '(%s) %s ' % ( self.code, self.name )
     
    def get_postions_structures(self):
        return self.structure_set.values('position')   

    def structure_count(self):
        return self.structure_set.count()         


class Location(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=30)
    status = models.BooleanField(default=True)
    start_date = models.DateField(null=False, blank=False)
    group = models.CharField(max_length=3)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '(%s) %s ' % ( self.code, self.name )

    def structure_count(self):
        return self.structure_set.count()    


class BusinessUnit(models.Model):
    code = models.CharField(unique=True, max_length=32)
    name = models.CharField(max_length=30)
    status = models.BooleanField(default=True)
    start_date = models.DateField(null=False, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '(%s) %s ' % ( self.code, self.name )

    def structure_count(self):
        return self.structure_set.count()

    def get_structures(self):
        return self.structure_set.all()

    def get_postions_structures(self):
        return self.structure_set.values('position')            


class Departament(models.Model):

    code = models.CharField(unique=True, max_length=32)
    name = models.CharField(max_length=30)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    head_boss = models.CharField(max_length=10, null=True, blank=True)
    status = models.BooleanField(default=True)
    start_date = models.DateField(null=False, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '(%s) %s ' % ( self.code, self.name )



class Position(models.Model):
    class Meta:
           unique_together = (('company','code'),)
 
    company = models.ForeignKey(to='organizational.Company', null=True, blank=True, on_delete=models.SET_NULL)
    code = models.CharField( max_length=20)
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    business_unit = models.ForeignKey("BusinessUnit", null=True, blank=True, on_delete=models.SET_NULL)
    departament = models.ForeignKey("Departament", null=True, blank=True, on_delete=models.SET_NULL)
    cost_center = models.ForeignKey("CostCenter", null=True, blank=True, on_delete=models.SET_NULL)
    division = models.ForeignKey("Division", null=True, blank=True, on_delete=models.SET_NULL)
    location = models.ForeignKey("Location", null=True, blank=True, on_delete=models.SET_NULL)

    status = models.BooleanField(default=True)
    start_date = models.DateField(null=False, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    perposition = models.ManyToManyField(to='equipments.Equipment',
                                         through='equipments.PerPosition',
                                         related_name='Equipment_position')

    def __str__(self):
        return '(%s) %s ' % ( self.code, self.name )

    def get_ocupate(self):
        #objects.filter(group=group).order_by('-added')[0]
        structures = self.structure_set.all()
        if structures:
            last_structure = structures.latest('id')
            if last_structure:
                return last_structure.employee
        else:
            return ''



class CostCenter(models.Model):

    class Meta:
        unique_together = (('company','code'),)

    company = models.ForeignKey(to='organizational.Company', null=True, blank=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=30)
    status = models.BooleanField(default=True)
    start_date = models.DateField(null=False, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '(%s) %s ' % ( self.code, self.name )


class structure(models.Model):
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(to='organizational.Company', null=True, blank=True, on_delete=models.SET_NULL)
    division = models.ForeignKey("Division", null=True, blank=True, on_delete=models.SET_NULL)
    location = models.ForeignKey("Location", null=True, blank=True, on_delete=models.SET_NULL)
    businessUnit = models.ForeignKey("BusinessUnit", null=True, blank=True, on_delete=models.SET_NULL)
    departament = models.ForeignKey("Departament", null=True, blank=True, on_delete=models.SET_NULL)
    position = models.ForeignKey("Position", null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(default=datetime.strptime("9999-12-31","%Y-%m-%d"), auto_now=False, auto_now_add=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('company','employee','start_date'))

    def position_name(self):
        return '%s' % (self.position.name)

    def __str__(self):
        return '%s - %s ' % ( self.position, self.employee ) 
           