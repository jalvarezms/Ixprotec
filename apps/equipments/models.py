from django.db import models
from apps.elements.models import Classification
from apps.sizes.models import Area,Size
import os
from django_serializable_model import SerializableModel
# Create your models here.

class Equipment(models.Model):
    DIARY = -1
    FOR_DAMAGE = 0
    EVERY_ONE_MONSTH = 1 
    EVERY_TWO_MONSTH = 2
    EVERY_TREE_MONSTH = 3
    EVERY_FOUR_MONSTH = 4
    EVERY_SIX_MONSTH = 6
    EVERY_ONE_YEAR = 12
    EVERY_TWO_YEAR = 24

    FREQUENCY_OF_CHANGE_CHOICES = [
        (DIARY,'Daily(1 day)' ),
        (FOR_DAMAGE,'Only For Damage'),
        (EVERY_ONE_MONSTH,'Monthly (30 days)'),
        (EVERY_TWO_MONSTH,'Every TWO (02) months'),
        (EVERY_TREE_MONSTH,'Every TREE (03)months'),
        (EVERY_FOUR_MONSTH,'Every FOUR (04)months'),
        (EVERY_SIX_MONSTH,'Every SIX (06) months'),
        (EVERY_ONE_YEAR,'Annually (12 months)'),
        (EVERY_TWO_YEAR,'Every 02 Years (02 years)'),
        ]

    code = models.CharField(unique=True, max_length = 10 , null=True)
    name = models.CharField(max_length=80, null=True)
    element_classification = models.ForeignKey(Classification,null=True,blank=True, on_delete=models.SET_NULL)
    area = models.ForeignKey(Area , null=True,blank=True, on_delete=models.SET_NULL)    
    time_of_life = models.IntegerField( blank=True, null=True)
    description = models.TextField( null=True, blank=True)
    mantenace_cleaning = models.TextField(null=True)
    certification = models.CharField(max_length=30, null=True)
    mode_use = models.TextField( null=True, blank=True)
    status = models.BooleanField(null=True , blank=True)
    required_inspection = models.BooleanField( default=True)
    #check_mode_uso = models.BooleanField( default=False)
    #check_mantenace_cleaning = models.BooleanField( default=False)
    #check_condition = models.BooleanField( default=False)
    frequency_of_change =  models.IntegerField(choices=FREQUENCY_OF_CHANGE_CHOICES, default=FOR_DAMAGE)
    is_disposable = models.BooleanField( default=False)
    position = models.ManyToManyField(to='organizational.Position', through='PerPosition', related_name='Equipment_position')
    company  = models.ForeignKey(to='organizational.Company',  null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='uploads/equipments/profile/',null=True, blank=True, verbose_name='image_')
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)

    
      

    def __str__(self):
        return '(%s-%s-%s) %s' % (self.element_classification.element_type.code,self.element_classification.code, self.code,self.name )

    def get_element_type_name(self):
         return '(%s) %s' % (self.element_classification.element_type.code, self.element_classification.element_type.name )  

    def get_element_type_description(self):
         return '%s' % (self.element_classification.element_type.description )     

    def get_element_class_description(self):
         return '%s' % (  self.element_classification.description )      

    def get_element_class_name(self):
         return '(%s) %s' % (self.element_classification.code, self.element_classification.name )  

    def get_documents(self):
        return self.document_set.all().order_by('-modified_date')  

    def get_firts_documents(self):
        return self.document_set.all()

    def get_prim_doc(self):
        return self.document_set.all().order_by('-modified_date').first() 

    def get_items_inspection(self):
        return self.itemsinspection_set.all().order_by('-modified_date')  

    def get_items_inspection_count(self):
        return self.itemsinspection_set.all().count()
    
    def frequency_of_change_text(self):      
        for choice in self.FREQUENCY_OF_CHANGE_CHOICES:
            if choice[0] == self.frequency_of_change:
                return choice[1]
        return self.FREQUENCY_OF_CHANGE_CHOICES[1][1] 
        #return self.FREQUENCY_OF_CHANGE_CHOICES[self.frequency_of_change]    
class Brand(models.Model):
    code = models.CharField(unique=True,max_length = 10 , null=True)
    name = models.CharField(max_length=30, null=True)
    create_date = models.DateTimeField(auto_now_add=True)    
    modified_date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return '%s' % (self.name)
    

class Supply(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_UNISEX = 2
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_UNISEX,'Unisex')]
    code = models.CharField(unique=True,max_length = 15 , null=True)
    equipment = models.ForeignKey(Equipment , null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    description = models.TextField( null=True, blank=True)
    size = models.ForeignKey(Size,null=True,blank=True, on_delete=models.SET_NULL)
    color = models.ForeignKey(to='equipments.color',null=True,blank=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand ,null=True,blank=True, on_delete=models.SET_NULL)
    material = models.TextField(max_length=30, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=GENDER_UNISEX)
    unid_content = models.IntegerField( default=1, blank=False, null=False)
    status = models.BooleanField(null=True, blank=True, default=True) 
    company     = models.ForeignKey(to='organizational.Company',  null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)

           

    def __str__(self):
        return '%s %s %s' % (self.code, self.equipment,self.name)

    def natural_key(self):
        return django_sub_dict(self)    
        
    def gender_text(self):        
        return self.GENDER_CHOICES[self.gender][1]

    def gender_icon_class(self):
        GENDER_ICONS = ["fa fa-male text-blue-darker","fa fa-female text-pink-darker","fa fa-venus-mars .text-green-darker"]    
        return GENDER_ICONS[self.gender]

    def status_text(self):
        return {True: 'Activated',False: 'Deactivated'}[self.status]    

    def get_documents(self):
        return self.document_set.all     
        
    def get_images(self):
        return self.photo_set.all   

    def get_video(self):
        return self.equipment.video_set.all

    def get_photo_url(self):
        return self.equipment.image.url    

    def get_photo(self):
        return self.equipment.image        

    def equipment_name(self):
        return '(%s) %s' % (self.equipment.code, self.equipment.name)    

    def equipment_description(self):       
        return '%s' % (self.equipment.description)      

    def get_photo(self):
        return self.equipment.image   

    def get_post_invetary(self):
        movement = self.movement_set.latest('id')
        if movement:
          return  movement.post_inventory
        return  0   

    def get_post_invetary_for_warehouse(self,warehouse_id):    
        movement = self.movement_set.filter(warehouse_id=warehouse_id)
        if movement:
            movement = movement.latest('id')
            return  movement.post_inventory
        return  0 
    def get_delivered_date(self):
        delivered =  self.delivereddetail_set.all() 
        delivered = delivered.latest('id')
        return delivered.modified_date 

class Color(models.Model):
    name = models.CharField(unique=True,max_length=20, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)
    def __str__(self):
        return '%s' % (self.name)

  

class PerPosition(models.Model):
    position = models.ForeignKey(to='organizational.Position' , null=True,blank=True, on_delete=models.CASCADE, related_name='position_equipment')
    equipment = models.ForeignKey(Equipment , null=True,blank=True, on_delete=models.CASCADE)
    description = models.TextField( null=True, blank=True)
    maximum = models.IntegerField(null=True)
    start_date = models.DateTimeField(null=True, blank=True)    
    end_date = models.DateTimeField(null=True, blank=True)  
    inspection_period = models.IntegerField(null=True)
    color = models.CharField(max_length=30, null=True)    
    company     = models.ForeignKey(to='organizational.Company',  null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)

class Photo(models.Model):
    equipment_by = models.ForeignKey(Equipment , null=True,blank=True, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='uploads/equipments/photos/',null=True, blank=True, verbose_name='photo_')
    title     = models.CharField(max_length=130,null=True)    
    description = models.TextField(max_length=850,null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)

    def extension(self):
        name, extension = os.path.splitext(self.document.name)
        return extension

class Video(models.Model):
    equipment_by = models.ForeignKey(Equipment, null=True,blank=True, on_delete=models.SET_NULL)
    video = models.CharField(max_length=200,null=False, blank=False)
    title     = models.CharField(max_length=150,null=True)
    description = models.TextField(max_length=800,null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)
  
class Document(models.Model):
    equipment_by = models.ForeignKey(Equipment , null=True,blank=True, on_delete=models.CASCADE)
    document = models.FileField( upload_to='uploads/equipments/documents/', null=True, blank=True, verbose_name='doc_' ,max_length=100)
    title     = models.CharField(max_length=130,null=True)
    description = models.TextField(max_length=850,null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)
    
    def extension(self):
        name, extension = os.path.splitext(self.document.name)
        return extension

class ItemsInspection(models.Model):
    equipment = models.ForeignKey(Equipment , null=True,blank=True, on_delete=models.CASCADE)
    check     = models.CharField(max_length=250,null=False)
    corrective_action = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True,  null=True)    
    modified_date = models.DateTimeField( auto_now=True, blank=True,  null=True)            