from django.conf.urls import url
from django.urls import  include, path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from .views import ListProvider,CreateProvider,UpdateProvider,DeleteProvider
from apps.inventories.views import *

app_name = 'inventories'

urlpatterns = [
    path('configurations/provider/list',ListProvider.as_view(), name='list_providers'),
    path('configurations/provider/edit/<int:pk>',UpdateProvider.as_view(), name='provider_edit'),
    path('configurations/provider/create',CreateProvider.as_view(), name='provider_create'),
    path('provider/delete',DeleteProvider.as_view(), name='provider_delete'),
    path('pending_request', TemplateView.as_view(template_name='pending_request.html'), name='pending_request'),
    path('inventory_output_completed', TemplateView.as_view(template_name='completed_request.html'), name='completed_request'),
    path('output_detail', TemplateView.as_view(template_name='output_detail.html'), name='output_detail'),
    path('inventory/entry/list', InventoryEntryList.as_view() , name='inventory_entry_list'),
    path('inventory/entry/create',InventoryEntryCreate.as_view(), name='inventory_entry_create'),
    path('inventory/report/entry/<int:pk>',InventoryEntryReport.as_view(), name='inventory_entry_report'),
    path('inventory/entry/<int:pk>/details',InventoryEntryDetailCreate.as_view(), name='inventory_entry_detail_create'),
    path('inventory/entry/details/<int:pk>',InventoryEntryDetailUpdate.as_view(), name='inventory_entry_detail_update'),
    path('inventory/entry/details/delete',InventoryEntryDetailDelete.as_view(), name='inventory_entry_detail_delete'),
    path('inventory/entry/show/<int:pk>',InventoryEntryDetailShow.as_view(), name='inventory_entry_detail_show'),
    path('inventory/entry/delete',InventoryEntryDelete.as_view(), name='inventory_entry_delete'),
    path('inventory/entry/confirm/<int:pk>',InventoryEntryConfirm.as_view(), name='inventory_entry_confirm'),
    path('inventory/supplies/<int:warehouse_pk>/<int:supply_pk>',InventorySupplyList.as_view(), name='inventory_supply_list'),
    path('inventory/movements/<int:warehouse_pk>/<int:supply_pk>',InventoryMovementList.as_view(), name='inventory_movement_list'),
    path('stock/level/create/<int:pk>',StockLevelUpdate.as_view(), name='inventory_stock_level_update'),
    path('inventory/output/list', InventoryOutputList.as_view() , name='inventory_output_list'),
    path('inventory/output/detail/<int:pk>', InventoryOutputDetail.as_view() , name='inventory_output_detail'),
    path('output_detail_ajax', SupplyAjax.as_view() , name='output_detail_ajax'),
    path('output_detail_save', SaveOutput.as_view() , name='output_detail_save'),
    path('inventory/output/completed-list', CompletedOutputList.as_view() , name='inventory_output_completed'),
    path('inventory/output/completed-detail/<int:pk>', CompletedOutputDetail.as_view() , name='inventory_output_completed'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)