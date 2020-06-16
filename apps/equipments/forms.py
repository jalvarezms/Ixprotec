from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Equipment, Supply,PerPosition,Document,Photo, Video, ItemsInspection
from django.utils.translation import ugettext_lazy as _
class Equipment_Form(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'code',
            'name',
            'element_classification',
            'area',
            'frequency_of_change',
            'description', 
            'mantenace_cleaning',
            'certification',
            'required_inspection',
            'is_disposable',
            'mode_use',     
            'status',
            'image',       
        ]
        labels = {
            'code' : _('Code'),
            'name' : _('Name'),
            'element_classification' : _('Element Classification'),
            'area' : _('Body Area'),
            'frequency_of_change' : _('Frequency of Change'),
            'description' : _('Description'), 
            'mantenace_cleaning': _('Maintenance Cleaning'),
            'certification' : _('Certification'),
            'required_inspection':_('Required Inspection?'),
            'is_disposable':_('Is Disponsable?'),
            'mode_use' : _('Use Mode'),     
            'status': _('Status'),
            'image':_('Image Profile')  ,      
        }
        widgets = {
            'code' : forms.TextInput(attrs={'class':'form-control'}),   
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'element_classification' : forms.Select(attrs={'class':'form-control','required':'true'}),
            'area' : forms.Select(attrs={'class':'form-control'}),
            'frequency_of_change': forms.Select(attrs={'class':'form-control'}),           
            'description' : forms.Textarea(attrs={'class':'form-control', 'rows':'2'}),            
            'mantenace_cleaning' : SummernoteWidget(),
            'certification' : forms.TextInput(attrs={'class':'form-control'}),
            'mode_use' : SummernoteWidget(),
            'status': forms.CheckboxInput(attrs={'checked':''}),   
            'required_inspection':forms.CheckboxInput(),
            'is_disposable':forms.CheckboxInput(),
            'image': forms.FileInput(attrs={'class':'form-control-file form-control-sm'}),         
        }

class SupplyForm(forms.ModelForm):
    use_required_attribute  = True
    class Meta:
        model = Supply
        fields = [
            'company',
            'equipment',
            'code',
            'name',
            'description',
            'color',
            'size',
            'brand',
            'material', 
            'gender',
            'unid_content',
            'status',      
        ]
        labels = {
            'company':_('Entity legal'),
            'equipment':_('Equipment'),
            'code':_('Code'),
            'name':_('Name'),
            'description':_('Description'),
            'color':_('Color'),
            'size':_('Size'),
            'brand':_('Brand'),
            'material':_('Material'), 
            'gender':_('Gender'),
            'unid_content':_('Content unids'),
            'status':_('Status'),      
        }
        widgets = {
             'company': forms.Select(  attrs={'class':'form-control','required':'true'}),
            'equipment':forms.Select(attrs={'class':'form-control'}),
            'code':forms.TextInput(attrs={'class':'form-control'}), 
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control', 'rows':'2'}),
            'color':forms.Select(attrs={'class':'form-control'}),
            'size': forms.Select(attrs={'class':'form-control'}),
            'brand':forms.Select(attrs={'class':'form-control'}),
            'material':forms.TextInput(attrs={'class':'form-control'}), 
            'gender': forms.Select(attrs={'class':'form-control'}),
            'unid_content':forms.NumberInput(attrs={'class':'form-control'}),
            'status':forms.CheckboxInput(attrs={'class':'form-control'}), 
                    
        }

class PerPositionForm(forms.ModelForm):
    class Meta:
        model = PerPosition
        fields = [
            'position',
            'equipment',
            'description', 
            'maximum',
            'start_date', 
            'end_date', 
            'inspection_period', 
        ]
        labels = {
            'position' :_('Position'),
            'equipment' :_('Equipment'),
            'description' :_('Description'),
            'maximum' :_('Max Permited'),
            'start_date' :_('Start date'),
            'end_date' :_(' End Date'), 
            'inspection_period':_('Inspection Period'),
        }
        widgets = {
            'position' : forms.Select(attrs={'class':'form-control selectpicker', 'id':'Position', 'data-live-search':'true', 'data-style':'btn-white'}),   
            'equipment' : forms.Select(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control', 'rows':'2'}),
            'maximum' : forms.TextInput(attrs={'class':'form-control'}),
            'start_date': forms.TextInput(attrs={'class':'form-control','id':'ppsd', 'data-date-format':'yyyy-mm-dd'}),            
            'end_date' : forms.TextInput(attrs={'class':'form-control', 'id':'pped', 'data-date-format':'yyyy-mm-dd'}),            
            'inspection_period' : forms.TextInput(attrs={'class':'form-control'}),            
        }

class PerPositionUpdateForm(forms.ModelForm):
    class Meta:
        model = PerPosition
        fields = [
            'position',
            'equipment',
            'description', 
            'maximum',
            'start_date', 
            'end_date', 
            'inspection_period', 
        ]
        labels = {
            'position' :_('Position'),
            'equipment' :_('Equipment'),
            'description' :_('Description'),
            'maximum' :_('Max Permited'),
            'start_date' :_('Start date'),
            'end_date' :_(' End Date'), 
            'inspection_period':_('Inspection Period'),
        }
        widgets = {
            'position' : forms.Select(attrs={'class':'form-control', 'readonly':'readonly', 'disabled': 'disabled'}),   
            'equipment' : forms.Select(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control', 'rows':'2'}),
            'maximum' : forms.TextInput(attrs={'class':'form-control'}),
            'start_date': forms.TextInput(attrs={'class':'form-control','id':'ppsd', 'data-date-format':'yyyy-mm-dd'}),            
            'end_date' : forms.TextInput(attrs={'class':'form-control', 'id':'pped', 'data-date-format':'yyyy-mm-dd'}),            
            'inspection_period' : forms.TextInput(attrs={'class':'form-control'}),            
        }

class DocumentsCreateForm(forms.ModelForm):
      class Meta:
        model = Document
        fields = [
            'equipment_by',
            'document',
            'description',
            'title',
        ]

        labels = {
           'equipment_by':_('equipment'),
            'document':_('Attachament'),
            'description':_('Description'),
            'title':_('Title'),
        }
        widgets = {
            'equipment_by' : forms.Select(attrs={'class':'form-control', 'disabled':'true'}),   
            'document' : forms.FileInput(attrs={'class':'form-control'}),
            'title' : forms.TimeInput(attrs={'class':'form-control' }), 
            'description' : forms.Textarea(attrs={'class':'form-control','rows':'2' }), 
        }
        
class DocumentsUpdateForm(forms.ModelForm):
      class Meta:
        model = Document
        fields = [
            'equipment_by',
            'description',
            'title',
        ]

        labels = {
            'equipment_by':_('Equipment'),
            'description':_('Description'),
            'title':_('Title'),
        }
        widgets = {
            'equipment_by' : forms.Select(attrs={'class':'form-control', 'disabled':'true'}),  
            'title' : forms.TimeInput(attrs={'class':'form-control' }), 
            'description' : forms.Textarea(attrs={'class':'form-control','rows':'2' }), 
        }
            

class PhotoCreateForm(forms.ModelForm):
      class Meta:
        model = Photo
        fields = [
            'equipment_by',
            'photo',
            'description',
            'title',
        ]

        labels = {
           'equipment_by':_('equipment'),
            'photo':_('Attachament'),
            'description':_('Description'),
            'title':_('Title'),
        }
        widgets = {
            'equipment_by' : forms.Select(attrs={'class':'form-control', 'disabled':'true'}),   
            'photo' : forms.FileInput(attrs={'class':'form-control'}),
            'title' : forms.TimeInput(attrs={'class':'form-control' }), 
            'description' : forms.Textarea(attrs={'class':'form-control','rows':'2' }), 
        }
           
class PhotoUpdateForm(forms.ModelForm):
      class Meta:
        model = Photo
        fields = [
            'equipment_by', 
            'description',
            'title',
        ]

        labels = {
           'equipment_by':_('equipment'), 
            'description':_('Description'),
            'title':_('Title'),
        }
        widgets = {
            'equipment_by' : forms.Select(attrs={'class':'form-control', 'disabled':'true'}),   
            'title' : forms.TimeInput(attrs={'class':'form-control' }), 
            'description' : forms.Textarea(attrs={'class':'form-control','rows':'2' }), 
        }
           
class VideoCreateForm(forms.ModelForm):
      class Meta:
        model = Video
        fields = [
            'equipment_by',
            'video',
            'description',
            'title',
        ]

        labels = {
           'equipment_by':_('equipment'),
            'video':_('https://www.youtube.com/embed/'),
            'description':_('Description'),
            'title':_('Title'),
        }
        widgets = {
            'equipment_by' : forms.Select(attrs={'class':'form-control', 'disabled':'true'}),   
            'video' : forms.TextInput(attrs={'class':'form-control' }), 
            'title' : forms.TimeInput(attrs={'class':'form-control' }), 
            'description' : forms.Textarea(attrs={'class':'form-control','rows':'2' }), 
        }           

class VideoUpdateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'equipment_by',
            'video',
            'description',
            'title',
        ]

        labels = {
           'equipment_by':_('equipment'),
            'video':_('https://www.youtube.com/embed/'),
            'description':_('Description'),
            'title':_('Title'),
        }
        widgets = {
            'equipment_by' : forms.Select(attrs={'class':'form-control', 'disabled':'true'}),   
            'video' : forms.TextInput(attrs={'class':'form-control' }), 
            'title' : forms.TimeInput(attrs={'class':'form-control' }), 
            'description' : forms.Textarea(attrs={'class':'form-control','rows':'2' }), 
        }                  


class ItemsInspectionForms(forms.ModelForm):
    class Meta:
        model = ItemsInspection
        fields = [
           'equipment',
            'check',
            'corrective_action',
        ]

        labels = {
            'equipment':_('Equipment'),
            'check':_('Check Control'),
            'corrective_action':_('Corretive Actions'),
        }
        widgets = {
            'equipment' : forms.Select(attrs={'class':'form-control'}),   
            'check' : forms.TextInput(attrs={'class':'form-control' }), 
            'corrective_action' : forms.Textarea(attrs={'class':'form-control','rows':'2' }),
        }     