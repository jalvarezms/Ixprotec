from django import forms

from .models import Element_Type, Classification
from django.utils.translation import ugettext_lazy as _
class Element_Type_Form(forms.ModelForm):
    class Meta:
        model = Element_Type
        fields = [
            'code',
            'name',
            'description',            
        ]
        labels = {
            'code' :_( 'Code'),
            'name' :_( 'Name'),
            'description' :_( 'Description'), 
        }
        widgets = {
            'code' : forms.TextInput(attrs={'class':'form-control'}),
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control'}), 
        }

class Element_Classification_Form(forms.ModelForm):
    class Meta:
        model = Classification
        fields = [
            'code',
            'name',
            'description',
            'status',
            'element_type',            
        ]
        labels = {
            'code ': _('Code'),
            'name' :_( 'Name'),
            'description' :_( 'Description'),
            'status' :_( 'Status'),
            'element_type' :_( 'Element Type'), 
        }
        widgets = {
            'code' : forms.TextInput(attrs={'class':'form-control'}),
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control'}),
            'status' : forms.CheckboxInput(attrs={'checked':'', 'value':'1'} ),
            'element_type' : forms.Select(attrs={'class':'form-control'}), 
        }