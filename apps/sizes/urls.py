from django.conf.urls import url
from django.urls import  include, path

from .views import BodyAreaList,BodyAreaCreate,BodyAreaUpdate,BodyAreaDelete, SizeList,SizeCreate,SizeUpdate,SizeDelete

app_name = 'sizes'
urlpatterns = [
    path('configurations/body-area/list', BodyAreaList.as_view(), name='body_area_list'),
    path('configurations/body-area/create', BodyAreaCreate.as_view(), name='body_area_create'),
    path('configurations/body-area/edit/<int:pk>/', BodyAreaUpdate.as_view(), name='body_area_edit'),
    path('body_area/delete/', BodyAreaDelete.as_view(), name='body_area_delete'),
    path('configurations/size/list', SizeList.as_view(), name='body_size_list'),
    path('configurations/size/create', SizeCreate.as_view(), name='body_size_create'),
    path('configurations/size/edit/<int:pk>/', SizeUpdate.as_view(), name='body_size_edit'),
    path('size/delete/', SizeDelete.as_view(), name='body_size_delete'),
]
