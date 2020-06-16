from django.contrib import admin
from apps.elements.models import Classification,Element_Type

admin.site.register(Element_Type)
admin.site.register(Classification)
