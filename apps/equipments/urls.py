from django.conf.urls import url
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from .views import *

app_name = 'equipments'
urlpatterns = [
    path('configurations/equipment/create', EquipmentCreate.as_view(), name='equipment_create'),
    path('configurations/equipment/index', EquipmentList.as_view(), name='equipment_list'),
    path('configurations/equipment/update/<int:pk>/', EquipmentUpdate.as_view(), name='equipment_update'),
    path('configurations/equipment/inspection/items/<int:pk>/', EquipmentInspetionItem.as_view(), name='equipment_inspetion_items'),
    path('configurations/equipment/inspection/items/update/<int:pk>/', EquipmentInspetionItemUpdate.as_view(), name='equipment_inspetion_items_update'),
    path('configurations/equipment/inspection/delete/', EquipmentInspetionItemDelete.as_view(), name='equipment_inspetion_items_delete'),
    path('equipment_delete', EquipmentDelete.as_view(), name='equipment_delete'),
    path('configurations/supplies/index', SupplyList.as_view(), name='supply_list'),
    path('configurations/supplies/create', SupplieCreateView.as_view(), name='supply_create'),
    path('configurations/supplies/edit/<int:pk>/', SupplyUpdate.as_view(), name='supply_edit'),
    path('supplies/delete/', SupplyDelete.as_view(), name='supply_delete'),
    path('configurations/perposition/index', PerPositionList.as_view(), name='perposition_list'),
    path('perposition/create', AsignEquipment.as_view(), name='perposition_create'),
    path('perposition_delete', PerPositionDelete.as_view(), name='perposition_delete'),
    path('perposition_save', PerPositionSave.as_view(), name='perposition_save'),
    path('perposition/update/<int:pk>/', PerpositionUpdate.as_view(), name='perposition_update'),
    path('asign_equipment_list', AsingEquipmentList.as_view(), name='asign_equipment_list'),
    path('<int:equipment>/documents/create/', EquipmentDocCreate.as_view(), name='equipment_doc_create'),
    path('<int:pk>/documents/show/', EquipmentDocShow.as_view(), name='equipment_doc_show'),
    path('documents/update/<int:pk>', EquipmentDocEdit.as_view(), name='equipment_doc_update'),
    path('documents/delete/', EquipmentDocDelete.as_view(), name='equipment_doc_delete'),
    path('<int:equipment>/image/create/', EquipmentImgCreate.as_view(), name='equipment_img_create'),
    path('<int:pk>/image/index/', EquipmentImgIndex.as_view(), name='equipment_img_index'),
    path('image/update/<int:pk>', EquipmentImgEdit.as_view(), name='equipment_img_update'),
    path('image/delete/', EquipmentImgDelete.as_view(), name='equipment_img_delete'),
    path('get', EquipmentGetJx.as_view(), name='equipment_getjx'),
    path('supply/get', SupplyGetJx.as_view(), name='supply_getjx'),
    path('<int:pk>/video/show/', EquipmentVideoShow.as_view(), name='equipment_video_show'),
    path('video/update/<int:pk>', EquipmentVideoEdit.as_view(), name='equipment_video_update'),
    path('<int:equipment>/video/create/', EquipmentVideoCreate.as_view(), name='equipment_video_create'),
    path('video/delete/', EquipmentVideoDelete.as_view(), name='equipment_video_delete'),
]