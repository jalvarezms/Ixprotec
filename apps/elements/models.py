from django.db import models

# Create your models here.
class Element_Type(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.TextField(max_length=30)
    description = models.TextField(max_length=250)
    create_date = models.DateTimeField(auto_now_add=True)    
    modified_date = models.DateTimeField( auto_now=True)
    def __str__(self):
        return '(%s)  %s ' % ( self.code, self.name)


class Classification(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.TextField(max_length=50)
    description = models.TextField(max_length=250)
    status = models.BooleanField(default=False)
    element_type = models.ForeignKey(Element_Type, null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)    
    modified_date = models.DateTimeField( auto_now=True)
    def __str__(self):
        return '(%s)  %s' % (self.code, self.name)
