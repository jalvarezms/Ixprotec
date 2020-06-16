from django import forms

from apps.requests.models import RequestType, EmployeeRequest,DetailRequest, Status
from django.utils.translation import ugettext_lazy as _
class RequestTypeForm(forms.ModelForm):
    class Meta:
        model = RequestType
        fields = [
            'code',
            'name',
            'detail',  
            'status', 
            'element_type',
            'element_classification',         
        ]
        labels = {
            'code' : _('Code'),
            'name' :_( 'Name'),
            'detail' :_( 'Description'), 
            'status' :_( 'Status'),
            'element_type':_( 'Element Type'),
            'element_classification':_( 'Element Classification'),
        }
        widgets = {
            'code' : forms.TextInput(attrs={'class':'form-control'}),
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'detail' : forms.Textarea(attrs={'class':'form-control', 'rows':'2'}), 
            'status' : forms.CheckboxInput(attrs={'class':'form-control', 'checked':''}),
            'element_type' : forms.Select(attrs={'class':'form-control'}),
            'element_classification' : forms.Select(attrs={'class':'form-control ec-tags', 'multiple' : 'multiple'}),
            
        }

class EmployeeRequestForm(forms.ModelForm):
    class Meta:
        model = EmployeeRequest
        fields = [
            'request_type',       
        ]
        labels = {
            'request_type' :_( 'Request Type'),
        }
        widgets = {
            'request_type' : forms.Select(attrs={'class':'form-control'}),            
        }
class  EmployeeRequestCreateForm(forms.ModelForm):
    class Meta:
        model = EmployeeRequest
        fields = [
            'request_type', 
            'position',
            'status_request',
            'employee',
            'observation',
        ]
        labels = {
            
            'request_type':_( 'Request Type'), 
            'position':_( 'Position'),
            'status_request':_( 'status_request'),
            'employee':_( 'Employee'),
            'observation':_( 'Observation'),
        }
        widgets = {
            
            'request_type':forms.Select(attrs={'class':'form-control'}), 
            'position':forms.Select(attrs={'class':'form-control'}),
            'employee':forms.Select(attrs={'class':'form-control'}),
            'status_request':forms.TextInput(attrs={'class':'form-control'}),
            'observation':forms.Textarea(attrs={'class':'form-control','rows':'2','placeholder':'request elements protection'}),          
        }

class  DetailRequestCreateForm(forms.ModelForm):
    class Meta:
        model = DetailRequest
        fields = [
            'employee_request',
            'equipment',
            'assigned_size', 
            'total',
            'color'
        ]
        labels = {
            'employee_request':_( 'Request'),
            'equipment':_( 'Equipment'),
            'assigned_size':_( 'Size'), 
            'total':_( 'Total'),
            'color':_( 'Color')
        }
        widgets = {
            'employee_request': forms.TextInput(attrs={'class':'form-control'}),
            'equipment': forms.Select(attrs={'class':'form-control select2-data'}),
            'assigned_sizen':forms.Select(attrs={'class':'form-control'}),
            'color':forms.Select(attrs={'class':'form-control'}),
            'total':forms.NumberInput(attrs={'class':'form-control','value':'1'}),          
        }   

class  RequestApprovalFlowForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = [
            'level',
            'observation',
            'status', 
            'employee_request',
            'employee'
        ]
        labels = {
            'employee_request':_( 'Request'),
            'observation':_( 'Observation'),
            'status':_( 'Status'), 
            'employee_request':_( 'Request'),
            'employee':_( 'Employee')
        }
        widgets = {
            'employee_request': forms.TextInput(attrs={'class':'form-control'}),
            'observation': forms.Textarea(attrs={'class':'form-control '}),
            'status':forms.CheckboxInput(attrs={'class':'form-control', 'checked':''}),
            'employee_request':forms.TextInput(attrs={'class':'form-control'}),
            'employee':forms.TextInput(attrs={'class':'form-control','value':'4'}),          
        } 