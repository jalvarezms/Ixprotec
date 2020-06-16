from django.contrib import admin
from apps.organizational.models import Company, Division, Departament,BusinessUnit,CostCenter, Position, Location,structure

from import_export.admin import ImportExportModelAdmin,ImportMixin ,ImportExportMixin
from apps.organizational.forms import CostCenterImportForm,CustomConfirmImportForm
from .resources import CompanyResource, DivisionResource, LocationResource, BusinessUnitResource, PositionUnitResource, DepartamentResource, CostCenterResource, StructureResource

admin.site.register(Company)
admin.site.unregister(Company)
admin.site.register(Division)
admin.site.unregister(Division)

admin.site.register(Location)
admin.site.unregister(Location)

admin.site.register(BusinessUnit)
admin.site.unregister(BusinessUnit)

admin.site.register(Departament)
admin.site.unregister(Departament)

admin.site.register(Position)
admin.site.unregister(Position)

admin.site.register(CostCenter)
admin.site.unregister(CostCenter)

admin.site.register(structure)
admin.site.unregister(structure)

class CompanyAdmin(ImportExportModelAdmin):
    resource_class = CompanyResource

class DivisionAdmin(ImportExportModelAdmin):
    resource_class = DivisionResource    

class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource    

class BusinessUnitAdmin(ImportExportModelAdmin):
    resource_class = BusinessUnitResource    

class DepartamentAdmin(ImportExportModelAdmin):
    resource_class = DepartamentResource    

class CostCenterAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = CostCenterResource    
    def get_import_form(self):        
        return CostCenterImportForm

    def get_confirm_import_form(self):
        return CustomConfirmImportForm

    def get_form_kwargs(self, form, *args, **kwargs):
        if isinstance (form, CostCenterImportForm):
            if form.is_valid():
                company = form.cleaned_data['company']
                kwargs.update({'company': company.id})
        elif isinstance (form, CustomConfirmImportForm): 
            if form.is_valid():     
                company = form.cleaned_data['company']
                kwargs.update({'company': company.id})
        return kwargs

class CostCenterAdmins(ImportExportModelAdmin):
    resource_class = CostCenterResource  

class PositionAdmin(ImportExportModelAdmin):
    resource_class = PositionUnitResource    

class StructureAdmin(ImportExportModelAdmin):
    resource_class = StructureResource            

admin.site.register(Company, CompanyAdmin)    
admin.site.register(Division, DivisionAdmin) 
admin.site.register(Location, LocationAdmin) 
admin.site.register(BusinessUnit, BusinessUnitAdmin) 
admin.site.register(Departament, DepartamentAdmin) 
admin.site.register(CostCenter, CostCenterAdmin) 
#admin.site.register(CostCenter, CostCenterAdmins) 

admin.site.register(Position, PositionAdmin) 
admin.site.register(structure, StructureAdmin) 



