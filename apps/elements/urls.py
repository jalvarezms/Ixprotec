from django.conf.urls import url
from django.urls import path,include
from . import views

from .views import TypeCreate, TypeList, TypeUpdate, TypeDelete, ClassificationCreate, ClassificationList, ClassificationUpdate,\
					ClassificationDelete,select_options_class_for_type

app_name = 'elements'
urlpatterns = [
	path('configurations/type/create', TypeCreate.as_view(), name='type_create'),
	path('configurations/type/list', TypeList.as_view(), name='type_list'),
	path('configurations/type/update/<int:pk>/', TypeUpdate.as_view(), name='type_update'),
	path('type_delete', TypeDelete.as_view(), name='type_delete'),
	path('configurations/classification/create', ClassificationCreate.as_view(), name='classification_create'),
	path('configurations/classification/list', ClassificationList.as_view(), name='classification_list'),
 	path('configurations/classification/update/<int:pk>/', ClassificationUpdate.as_view(), name='classification_update'),
 	path('classification_delete', ClassificationDelete.as_view(), name='classification_delete'),
	path('ajax/select_options_class_for_type', views.select_options_class_for_type, name='select_options_class_for_type'),
]