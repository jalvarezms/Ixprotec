from django import forms
from .models import  AssignedSize
from django.utils.translation import ugettext_lazy as _
class Assigned_Size_Form(forms.ModelForm):
    class Meta:
        model = AssignedSize
        fields = [
            'size', 
            'employee',         
        ]
        labels = {
            'size': _('Size'),
            'employee' : _('employee'),  
        }
        widgets = {
            'size':forms.Select(),
            'employee':forms.Select(),

        }