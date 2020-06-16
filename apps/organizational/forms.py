from django import forms
from apps.organizational.models import CostCenter, Company
from django.utils.translation import ugettext_lazy as _
from import_export.forms import ImportForm,ConfirmImportForm

class CostCenterImportForm(ImportForm):    
    company = forms.ModelChoiceField( queryset=Company.objects.all(),required=True)


class CustomConfirmImportForm(ConfirmImportForm):
    company = forms.ModelChoiceField( queryset=Company.objects.all(),required=True)
