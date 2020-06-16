from django.contrib import admin

from .models import Delivered,DeliveredDetail

# Register your models here.

admin.site.register(Delivered)
admin.site.register(DeliveredDetail)