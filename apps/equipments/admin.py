from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from apps.equipments.models import Color, Equipment , Supply, Brand,PerPosition,Photo,Video,Document
from import_export.admin import ImportExportModelAdmin,ImportMixin ,ImportExportMixin
from .resources import EquipmentResource,PerPositionResource,SupplyResource
# Register your models here.

# class EquipmentAdmin(SummernoteModelAdmin):
#     summernote_fields = ('mode_use','mantenace_cleaning')


admin.site.register(Equipment)
admin.site.unregister(Equipment)

admin.site.register(Brand)

admin.site.register(Supply)
admin.site.unregister(Supply)

admin.site.register(Color)

admin.site.register(PerPosition)
admin.site.unregister(PerPosition)

admin.site.register(Photo)
admin.site.register(Video)
admin.site.register(Document)


class EquipmentAdmin(ImportExportModelAdmin,SummernoteModelAdmin):
    summernote_fields = ('mode_use','mantenace_cleaning')
    resource_class = EquipmentResource

class PerPositionAdmin(ImportExportModelAdmin):
    resource_class = PerPositionResource

class SupplyAdmin(ImportExportModelAdmin):
    resource_class = SupplyResource


admin.site.register(Equipment,EquipmentAdmin)
admin.site.register(PerPosition,PerPositionAdmin)
admin.site.register(Supply,SupplyAdmin)