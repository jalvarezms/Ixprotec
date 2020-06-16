from django.conf.urls import url
from django.urls import path,include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from .views import *

app_name = 'requests'
urlpatterns = [
	path('configurations/type/create', RequestTypeCreate.as_view(), name='request_type_create'),
	path('configurations/type/list', RequestTypeList.as_view(), name='request_type_list'),
	path('configurations/type/update/<int:pk>/', RequestTypeUpdate.as_view(), name='request_type_update'),
	path('type_delete', RequestsTypeDelete.as_view(), name='request_type_delete'),
	path('supplies-request', EmployeeRequestList.as_view(), name='supplies_request'),
	path('supplies-request/create/<int:pk>/', EmployeeRequestCreate.as_view(), name='supplies_request_create'),
	path('supplies-request/create/<int:pk>/details', EmployeeRequesDetailsCreate.as_view(), name='employee_request_detail_create'),
	path('supplies-request/create/<int:pk>/sender', EmployeeRequesSenderApproval.as_view(), name='employee_request_sender_approval'),
	path('supplies_request_delete/', EmployeeRequestDelete.as_view(), name='employee_request_delete'),
	path('supplies-request/create/details/edit/<int:pk>', EmployeeRequesDetailsUpdate.as_view(), name='employee_request_detail_edit'),
	path('supplies_request_create/details/delete', EmployeeRequesDetailsDelete.as_view(), name='employee_request_detail_delete'),
	path('supplies-request/create/<int:pk>/details/list', EmployeeRequesDetailsList.as_view(), name='employee_request_detail_list'),
	path('manage/list', ManageRequestList.as_view(), name='manage_request_list'),
	path('manage/show/<int:pk>', ManageRequesShow.as_view(), name='manage_request_show'),
	path('manage/approval/<int:pk>/<int:pks>', ManageRequesApproval.as_view(), name='manage_request_approval'),
	path('delivered_items', TemplateView.as_view(template_name='delivered_items.html'), name='delivered_items'),
	path('my_delivered', TemplateView.as_view(template_name='my_delivered.html'), name='my_delivered')
]