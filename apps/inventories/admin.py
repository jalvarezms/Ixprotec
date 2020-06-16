from django.contrib import admin
from apps.inventories.models import Provider, ReasonMovement, CheckEntry, CheckinDetail,Movement,CheckOutPut,CheckOutPutDetail

# Register your models here.

admin.site.register(Provider)
admin.site.register(ReasonMovement)
admin.site.register(CheckEntry)
admin.site.register(CheckinDetail)
admin.site.register(Movement)
admin.site.register(CheckOutPut)
admin.site.register(CheckOutPutDetail)
