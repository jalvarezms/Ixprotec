from django.urls import path 
from django.urls import  include
from django.views.generic import TemplateView
from .views import ListHistoricalRecibed,ListHistoricalRequest,ListStorageinventory,ReportMatrizPPEforBusinessUnit,ReporFrequencyOfChangeEPP,NotificationList

app_name='reports' 

urlpatterns=[ 
    # path('Historic/', TemplateView.as_view(template_name="report1.html"),name="Historic"),
    path('report/recibed',ListHistoricalRecibed.as_view(),name="Historic_recibed"),
    path('report/request',ListHistoricalRequest.as_view(),name="Historic_request"),
    path('report/inventory',ListStorageinventory.as_view(),name="Historic_inventory"),
    path('report/matriz/EPP/business_units',ReportMatrizPPEforBusinessUnit.as_view(),name="report_matriz_ppe"),
    path('report/frequency_of_change/EPP/division',ReporFrequencyOfChangeEPP.as_view(),name="report_frequency_change_epp"),
    path('notification/list',NotificationList.as_view(),name="notification_list"),

]