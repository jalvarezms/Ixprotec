from django.urls import path, include
from django.contrib import admin
#from .api import router
from .views import *



app_name = "api" 

urlpatterns = [
    #path('', include(router.urls)),
    path('rest/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('company/', CompanyList.as_view()),
    path('division/',DivisionList.as_view() ),
    path('location/',LocationList.as_view() ),
    path('businessunit/',BusinessUnitList.as_view() ),
    path('departament/',DepartamentList.as_view() ),
    path('coscenter/',CostCenterList.as_view() ),
    path('position/',PositionList.as_view() ),
    path('structure/',StructureList.as_view() ),
    path('employee/',EmployeeList.as_view() ),
    path('areas/',AreaList.as_view()),
    path('sizes/',SizeList.as_view())

]



