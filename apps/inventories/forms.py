from django import forms
from .models import Provider, CheckEntry, CheckinDetail, StockLevel
from django.utils.translation import ugettext_lazy as _
class ProviderForms(forms.ModelForm):
    class Meta:
        model=Provider
        fields = [
            'name',
            'NIT',
            'Address',
            'PhoneNumber',
        ]
        labels = {
            'name' : _('Name'),
            'NIT' : _('NIT'),
            'Address' : _('Address'),
            'PhoneNumber' : _('Phone Number'),
        }
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}), 
            'NIT' : forms.TextInput(attrs={'class':'form-control'}), 
            'Address' : forms.TextInput(attrs={'class':'form-control'}), 
            'PhoneNumber' : forms.TextInput(attrs={'class':'form-control'}), 
        }
    
class CheckEntryCreateForms(forms.ModelForm):
    class Meta:
        model=CheckEntry
        fields = [
            'provider',
            'bill',
            'date_entry',
            'observation',
            'storer',
            'reason_movement',
            'warehouse',
        ]
        labels = {
            'provider':_('Provider'),
            'bill':_('Bill'),
            'date_entry':_('Date'),
            'observation':_('Observation'),
            'storer':_('Storer'),
            'reason_movement':_('Reason'),
            'warehouse':_('WareHouse'),
        }
        widgets = {
            'provider': forms.Select(attrs={'class':'form-control'}),
            'bill': forms.TextInput(attrs={'class':'form-control'}),
            'date_entry':forms.TextInput(attrs={'class':'form-control','value':'01/03/2020'}),
            'observation':forms.Textarea(attrs={'class':'form-control','rows':'2'}),
            'storer': forms.Select(attrs={'class':'form-control'}),
            'reason_movement': forms.Select(attrs={'class':'form-control'}),
            'warehouse':forms.Select(attrs={'class':'form-control'}),
        }

class CheckEntryDetailCreateForms(forms.ModelForm):
    class Meta:
        model=CheckinDetail
        fields = [
            'check_entry',
            'supply',
            'total',
            'location',
            'warraty_month',
            'expire_date',
        ]
        labels = {
            'check_entry':_('Inventory Entry'),
            'supply':_('Supply'),
            'total':_('Total'),
            'location':_('Warehouse location'),
            'warraty_month':_('Warranty'),
            'expire_date':_('Expire  Date'),
        }
        widgets = {
            'check_entry': forms.Select(attrs={'class':'form-control'}),
            'supply': forms.Select(attrs={'class':'form-control'}),
            'total':forms.NumberInput(attrs={'class':'form-control','value':1}),
            'location': forms.TextInput(attrs={'class':'form-control','value':'3C2'}),
            'warraty_month': forms.NumberInput(attrs={'class':'form-control','value':12}),
            'expire_date':forms.TextInput(attrs={'class':'form-control','value':'01/02/2022'}),
        }        

class StockLevelCreateForms(forms.ModelForm):
    class Meta:
        model = StockLevel       
        fields = [
            'warehouse',
            'supply',
            'minimum',
            'maximum',
           
        ]
        labels = {
            'warehouse':_('WareHouse'),
            'supply':_('Supply'),
            'minimum':_('Minimun'),
            'maximum':_('Maximum'),
            
        }
        widgets = {
            'warehouse': forms.Select(attrs={'class':'form-control'}),
            'supply': forms.Select(attrs={'class':'form-control'}),
            'minimum':forms.NumberInput(attrs={'class':'form-control','value':12}),
            'maximum': forms.NumberInput(attrs={'class':'form-control','value':12}),
            
        }        
