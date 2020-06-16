from django.db import models
from django_serializable_model import SerializableModel
from django.contrib.auth.models import User
from django.conf import settings

# from apps.organizational.models import Company
from django.db.models import F,Q,Exists


# Create your models here.

class Employee(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]

    code = models.CharField(unique=True, max_length=10)
    #company = models.ForeignKey(to='organizational.Company', null=True, blank=True, on_delete=models.SET_NULL)
    firts_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=40)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='uploads/employees/perfil/', null=True, blank=True, verbose_name='perfil')
    document = models.CharField(max_length=10, null=True, blank=True)
    number_doc = models.CharField(max_length=15, null=True, blank=True)
    sizes = models.ManyToManyField(to='sizes.Size', related_name="employee_assigned_sizes", through='AssignedSize')
    Birth_Place = models.CharField(max_length=30, null=True)
    Place_Residence = models.CharField(max_length=30, null=True)
    Address = models.CharField(max_length=30, null=True)
    Email = models.CharField(max_length=30, null=True)
    Phone = models.CharField(max_length=30, null=True)
    user_model = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def natural_key(self):
        return ({'firts_name':self.firts_name,'second_name': self.second_name,'gender': self.get_postion(),'photo':str(self.photo),'get_postion':self.get_postion()} )

    def allowed_fields(self):
        return [
                'firts_name',
                'second_name','gender',
                'photo','position','get_postion'
                ]  

    def __str__(self):
        return '%s-%s, %s ' % ( self.code, self.firts_name.upper(), self.last_name.upper())

    def get_short_name(self):
        return '%s %s' % (  self.firts_name.upper(), self.last_name.upper())
    
    def get_structure(self):
        return self.structure_set.all()

    def get_structure_last(self):
        return self.structure_set.latest('id')

    def get_postion(self):    
        structure = self.structure_set
        return structure.latest('id').position_name()

    def get_position(self):    
        structure = self.structure_set
        if structure:
            structure =  structure.latest('id') 
            return structure.position
        return ''

 

    def delivered(self):
        return self.delivered_employee.all()
    
    def request_status(self):
        return self.status_set.all()
     

class AssignedSize(models.Model):
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL )
    size = models.ForeignKey(to='sizes.Size', null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'size'], name='just_one_size_per_employee')
        ]

    def __str__(self):
        return '%s' % (self.size)
