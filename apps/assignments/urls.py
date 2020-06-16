from django.conf.urls import url
from django.urls import path,include

from .views import *

app_name = 'assignments'
urlpatterns = [
	path('inspections/list', InspectionList.as_view(), name='inspection_list'),
	path('inspections/select/', InspectionSelect.as_view(), name='inspection_select'),
	path('delivered_ajax', DeliveredAjax.as_view(), name='delivered_ajax'),
	path('inspections/view/<int:pk>', ViewInspection.as_view(), name='inspection_view'),
]