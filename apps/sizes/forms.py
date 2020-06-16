from django import forms
from .models import Area,Size

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields =[
            'code',
            'name',
            'description',
            'status',
        ]
        labels ={
            'code' : 'Code',
            'name' : 'Name',
            'description' : 'Description',
            'status' : 'Status',
        }
        widgets={
            'code': forms.TextInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
            'status':forms.CheckboxInput(attrs={'checked':''}),
        }
class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields =[
            'code',
            'gender',
            'body_area',            
            'name',
            'description',
            'status',
        ]
        labels ={
            'code':'Code',
            'gender': 'Gender',
            'body_area':'Area',
            'name':'Name',
            'description':'Description',
            'status':'Status',
            
        }
        widgets={
            'code': forms.TextInput(attrs={'class':'form-control'}),            
            'gender':forms.Select(attrs={'class':'form-control'}),    
            'body_area':forms.Select(attrs={'class':'form-control'}),        
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
            'status':forms.CheckboxInput(),
        }
