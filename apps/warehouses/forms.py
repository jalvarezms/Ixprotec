from django import forms
from .models import Warehouse,Storer


class WarehouseForm(forms.ModelForm):
    class Meta():
        model = Warehouse
        fields =[
            'name',
            'address',
            'phone_number',
            'company',
            'division',
            'departament',
        ]
        labels ={
            'name':'Name',
            'address':'Address',
            'phone_number':'Phone Number',
            'company':'Company',
            'division':'Division',
            'departament':'Departament',
        }
        widgets={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'company': forms.Select(attrs={'class':'form-control'}),
            'division': forms.Select(attrs={'class':'form-control'}),
            'departament': forms.Select(attrs={'class':'form-control'}),
            'status':forms.CheckboxInput(),
        }

class StorerForm(forms.ModelForm):
    class Meta():
        model=Storer
        fields =[
            'warehouse',
            'position',
            'grand_input',
            'grand_output',
            'status',
        ]
        labels ={
            'warehouse':'Warehouse',
            'position':'Position',
            'grand_input ':'Grand Input',
            'grand_output':'Grand Output',
            'status':'Status',
        }
        widgets={
            'warehouse': forms.Select(attrs={'class':'form-control'}),
            'position':forms.Select(attrs={'class':'form-control'}),
            'grand_input': forms.CheckboxInput(attrs={'class':'form-control'}),
            'grand_output': forms.CheckboxInput(attrs={'class':'form-control'}),
            'status':forms.CheckboxInput(),
        }

