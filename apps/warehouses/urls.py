from django.conf.urls import url
from django.urls import  include, path

from .views import WarehouseList,WarehousesCreate,WarehousesEdit,WarehouseDelete,AddResponsable,ResponsableUpdate,ResponsableDelete


app_name = 'warehouses'

urlpatterns = [
    path('configurations/warehouse/list', WarehouseList.as_view(), name='warehouse_list'),
    path('configurations/warehouse/create', WarehousesCreate.as_view(), name='warehouse_create'),
    path('configurations/warehouse/edit/<int:pk>/', WarehousesEdit.as_view(), name='warehouse_edit'),
    path('configurations/warehouse/addresponsable/<int:pk>/', AddResponsable.as_view(), name='add_responsable'),
    path('configurations/warehouse/responsable_update/<int:pk>/', ResponsableUpdate.as_view(), name='responsable_update'),
    path('warehouse/delete/', WarehouseDelete.as_view(), name='warehouse_delete'),
    path('configurations/addresponsable/delete/<int:pk>/', ResponsableDelete.as_view(), name='responsable_delete'),
]
