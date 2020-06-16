
from apps.organizational.models import *
from import_export import resources,fields
from apps.organizational.models import Company,Departament,Position, CostCenter, Division, Location, structure, BusinessUnit
from import_export.widgets import ForeignKeyWidget,BooleanWidget, DateWidget,DateTimeWidget

from import_export import widgets
from apps.employees.models import Employee

class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company
        import_id_fields  = ('code',)
        fields = ('code','name','status', 'start_date', 'country_code','country_name','city_name','telephone','address',)


class DivisionResource(resources.ModelResource):
    class Meta:
        model = Division
        import_id_fields  = ('code',)
        fields = ('code','name','status', 'start_date',)        


class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        import_id_fields  = ('code',)
        fields = ('code','name','status', 'start_date','group',)  


class BusinessUnitResource(resources.ModelResource):
    class Meta:
        model = BusinessUnit
        import_id_fields  = ('code',)
        fields = ('code','name','status', 'start_date',)

class PositionUnitResource(resources.ModelResource):
    company = fields.Field(
                    column_name='company',
                    attribute='company',
                    widget=ForeignKeyWidget(Company, 'code'))   
    departament = fields.Field(
                    column_name='departament',
                    attribute='departament',
                    widget=ForeignKeyWidget(Departament, 'code'))       

    business_unit = fields.Field(
                    column_name='business_unit',
                    attribute='business_unit',
                    widget=ForeignKeyWidget(BusinessUnit, 'code'))
    parent = fields.Field(
                    column_name='parent',
                    attribute='parent',
                    widget=ForeignKeyWidget(Position, 'code'))

    cost_center =  fields.Field(
                    column_name='cost_center',
                    attribute='cost_center',
                    widget=ForeignKeyWidget(CostCenter, 'code'))    
                     

    class Meta:
        model = Position
        import_id_fields  = ('company','code')
        fields = ('code','company','name','parent','business_unit','departament','status', 'start_date',)   
        skip_unchanged = True
        report_skipped = True
        use_transactions = True



class DepartamentResource(resources.ModelResource):
    parent = fields.Field(
            column_name='parent',
            attribute='parent',
            widget=ForeignKeyWidget(Departament, 'code')) 

    status = fields.Field(
        column_name='status',
        attribute='status',
        widget=widgets.BooleanWidget()) 
    
    class Meta:
        model = Departament
        import_id_fields  = ('code',)        
        fields = ('code','name','parent','head_boss','status', 'start_date',)                   

class CostCenterResource(resources.ModelResource):

    company = fields.Field(
                    column_name='company',
                    attribute='company',
                    widget=ForeignKeyWidget(Company, 'code'))                    
    class Meta:
        model = CostCenter
        import_id_fields  =['code','company']
        exclude = ('id', )
        fields = ('company','code','name','status', 'start_date',)
        skip_unchanged = True
        report_skipped = True
        use_transactions = True

class StructureResource(resources.ModelResource):
    employee = fields.Field(
                column_name='employee',
                attribute='employee',
                widget=ForeignKeyWidget(Employee, 'code')) 
    company = fields.Field(
                column_name='company',
                attribute='company',
                widget=ForeignKeyWidget(Company, 'code')) 
    division = fields.Field(
                column_name='division',
                attribute='division',
                widget=ForeignKeyWidget(Division, 'code'))
    location  = fields.Field(
                column_name='location',
                attribute='location',
                widget=ForeignKeyWidget(Location, 'code'))
    businessUnit  = fields.Field(
        
                column_name='businessUnit ',
                attribute='businessUnit',
                widget=ForeignKeyWidget(BusinessUnit, 'code'))
    departament  = fields.Field(
                column_name='departament',
                attribute='departament',
                widget=ForeignKeyWidget(Departament, 'code'))
    position  = fields.Field(
                column_name='position',
                attribute='position',
                widget=ForeignKeyWidget(Position, 'code'))

    start_date  = fields.Field(
                column_name='start_date',
                attribute='start_date',               
                widget=DateWidget( format =("%Y-%m-%d") ))
    end_date  = fields.Field(   
                column_name='end_date',
                attribute='end_date',               
                widget=DateWidget( format =("%Y-%m-%d") ))            
    class Meta:
        model = structure
        import_id_fields  = ('company','employee', 'start_date')
        fields = ('employee','company','division','location','businessUnit','departament','position', 'start_date','end_date')


