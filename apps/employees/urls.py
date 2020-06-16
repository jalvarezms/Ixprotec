from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView
from .views import MyDataList, RateElement,SizeEmployeeList,SizeEmployeeCreate,EquipmentDelete,SizeEmployeeUpdate,SizeAjax,DeliveredList,DeliveredDetailView, DeliveredPDF

app_name = 'employees'

urlpatterns = [
    path('rateit/<int:pk>', RateElement.as_view(),name="rate_it"),
    path('myData/', MyDataList.as_view(),name="my_data"),
    path('configure/yoursizes/', SizeEmployeeList.as_view(),name="configure_sizes_list"),
    path('configure/yoursizes/create/', SizeEmployeeCreate.as_view(),name="configure_sizes_create"),
    path('configure/yoursizes/delete/', EquipmentDelete.as_view(), name='configure_sizes_delete'),
    path('configure/yoursizes/update/<int:pk>', SizeEmployeeUpdate.as_view(), name='configure_sizes_update'),
    path('deliveries/list', DeliveredList.as_view(), name='delivered_list'),
    path('size_ajax', SizeAjax.as_view(), name='size_ajax'),
    path('deliveries/detail/<int:pk>', DeliveredDetailView.as_view(), name='delivered_detail'),
    path('deliveries/detail/<int:pk>/pdf', DeliveredPDF.as_view(), name='delivered_pdf'),
]