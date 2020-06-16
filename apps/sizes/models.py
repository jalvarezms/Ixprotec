from django.db import models
from apps.employees.models import Employee

from django_serializable_model import SerializableModel

# Create your models here.


class Area(models.Model):
    code = models.CharField(unique=True,max_length=10, null=False)
    name = models.TextField(max_length=20, null=True)
    description = models.TextField(max_length=50, null=True)
    status = models.BooleanField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '(%s) %s' % (self.code, self.name)
class Size(SerializableModel):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_UNISEX = 2
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_UNISEX,'Unisex')]
    code = models.CharField( max_length=10,null=False)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=GENDER_UNISEX)
    body_area = models.ForeignKey(Area,  on_delete=models.CASCADE, null=True, blank=True) 
    description = models.TextField(max_length=250, null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, default=True)    
    name = models.TextField(max_length=20, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['code','gender','body_area'],name='size_code_gender_body_area_unique'),
        ]
    

    def gender_text(self):        
        return self.GENDER_CHOICES[self.gender][1]

    def gender_icon_class(self):
        GENDER_ICONS = ["fa fa-male text-blue-darker","fa fa-female text-pink-darker","fa fa-venus-mars .text-green-darker"]    
        return GENDER_ICONS[self.gender]

    def __str__(self):
        return '(%s-%s) %s' % (self.code, self.GENDER_CHOICES[self.gender][1], self.name)
