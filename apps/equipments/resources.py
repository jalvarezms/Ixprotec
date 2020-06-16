from import_export import resources,fields
from .models import Equipment, PerPosition, Supply
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from apps.elements.models import Classification
from apps.sizes.models import Area
from apps.organizational.models import Position, Company
from .models import Color, Brand
from apps.sizes.models import Size

class EquipmentResource(resources.ModelResource):

    element_classification = fields.Field(
                                column_name='element_classification',
                                attribute='element_classification',
                                widget=ForeignKeyWidget(Classification, 'code'))
  
    area = fields.Field(
                                column_name='area',
                                attribute='area',
                                widget=ForeignKeyWidget(Area, 'code'))
    position = fields.Field(
                                column_name='position',
                                attribute='position',
                                widget=ManyToManyWidget(Position, 'code'))
 
    company = fields.Field(
                                column_name='company',
                                attribute='company',
                                widget=ForeignKeyWidget(Company, 'code'))
    class Meta:
        model = Equipment 
        import_id_fields = ('code',)
        fields = ('code','name','element_classification','area','time_of_life','description', 'mantenace_cleaning','certification','mode_use','status', 'required_inspection','frequency_of_change','is_disposable','position', 'image', 'create_date','modified_date',)



class PerPositionResource(resources.ModelResource):

    position = fields.Field(
                        column_name='position',
                        attribute='position',
                        widget=ForeignKeyWidget(Position, 'code'))

    equipment = fields.Field(
                        column_name='equipment',
                        attribute='equipment',
                        widget=ForeignKeyWidget(Equipment, 'code'))

    company = fields.Field(
                        column_name='company',
                        attribute='company',
                        widget=ForeignKeyWidget(Company, 'code'))
    
    class Meta:
        model = PerPosition
        fields = ('position', 'equipment','description','maximum','start_date','end_date','inspection_period','color','company','create_date','modified_date',)
  


class SupplyResource(resources.ModelResource):
    color = fields.Field(
                        column_name='color',
                        attribute='color',
                        widget=ForeignKeyWidget(Color, 'name'))

    size = fields.Field(
                        column_name='size',
                        attribute='size',
                        widget=ForeignKeyWidget(Size, 'code'))
    
    brand = fields.Field(
                        column_name='brand',
                        attribute='brand',
                        widget=ForeignKeyWidget(Brand, 'code'))

    company = fields.Field(
                        column_name='company',
                        attribute='company',
                        widget=ForeignKeyWidget(Company, 'code'))

    equipment = fields.Field(
                        column_name='equipment',
                        attribute='equipment',
                        widget=ForeignKeyWidget(Equipment, 'code'))

    class Meta:
        model = Supply
        import_id_fields = ('code',)
        report_skipped = True
        skip_unchanged = True
        fields = ('code','equipment','name','description','size','color','brand','material','gender','unid_content','status','company','create_date','modified_date')
        







 

