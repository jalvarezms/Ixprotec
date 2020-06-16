from django import forms

from .models import *
from django.utils.translation import ugettext_lazy as _
class EmployeeInspectionForm(forms.ModelForm):
    class Meta:
        model = EmployeeInspection
        fields = [
            'employee',          
        ]
        labels = {
            'employee' : _('Employee'),
        }
        widgets = {
            'employee' : forms.Select(attrs={'class':'form-control',}), 
        }