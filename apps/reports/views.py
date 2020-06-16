from django.shortcuts import render
from django.views.generic import View, CreateView,UpdateView,DeleteView,ListView, DetailView
from ..assignments.models import *
from ..requests.models import *
from ..inventories.models import *
from ..organizational.models import *
from ..elements.models import *
from ..equipments.models import *
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from notifications.models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _

class ListHistoricalRecibed(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = DeliveredDetail
    template_name = 'historical_recibed.html'

    def get_context_data(self, **kwargs):
        context = super(ListHistoricalRecibed, self).get_context_data(**kwargs)
        employee = self.request.user.employee
        deliv_ids = Delivered.objects.filter(employee = employee).values('id')
        # print(deliv_ids)
        supply_ids = DeliveredDetail.objects.filter(delivered_id__in = deliv_ids ).values('supply_id')
        delivery_details = DeliveredDetail.objects.filter(delivered_id__in = deliv_ids )

        data = delivery_details
        elements = []
        for d in data:
            elements.append([
                {
                    'type': 'image',
                    'content': d.supply.equipment.image.url
                },
                {
                    'type': 'code_name',
                    'content': {
                        'code':d.supply.code,
                        'name': d.supply.name
                    }
                },
                {
                    'type': 'label',
                    'content': [{'code':DeliveredDetail.STATUS_CHOICES[d.is_accept][1]}] 
                },
                {
                    'type': 'text',
                    'content': d.observation
                },
                {
                    'type': 'date',
                    'content': d.create_date
                },
                {
                    'type': 'text',
                    'content': d.expire_date
                },
                {
                    'type': 'employee_profile',
                    'content': d.delivered.deliverer.employee
                } 
            ])
        dataTable = {
            'card_tittle' : _('Items Delivery'),
            'headers': [_('Photo'), _('Supply'),_('Was accepted'),_('Observation'), _('Delivered Date'),_('Expire Date'), _('Delivered By')],
            'data': elements,
        }
        context['dataTable'] =  dataTable
        return context
class ListHistoricalRequest(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = EmployeeRequest
    template_name = 'historical_request.html'
    
    def get_context_data(self, **kwargs):
        context = super(ListHistoricalRequest, self).get_context_data(**kwargs)
        employee = self.request.user.employee
        data = employee.employeerequest_set.all()
        elements = []
        for d in data:
            elements.append([
                {
                    'type': 'label',
                    'content': [{'code':d.code}]
                },
                {
                    'type': 'employee_profile',
                    'content': d.employee
                },
                {
                    'type': 'code_name',
                    'content':{
                        'code':d.request_type.code,
                        'name':d.request_type.name
                    }                     
                },
                {
                    'type': 'label',
                    'content': [{ 'code': 'Approved'}]  
                },
                # {
                #     'type': 'code_name',
                #     'content': {'code': d.cost_center.name,'name':d.cost_center}
                # },
                {
                    'type': 'text',
                    'content': d.location
                },
                
                {
                    'type': 'text',
                    'content': d.observation 
                },
                
                {
                    'type': 'date',
                    'content': d.create_date
                }, 
                
            ])
        dataTable = {
            'card_tittle' : _('My Request Made'),
            'headers': [_('Code'), _('Employee'), _('Request Type'), _('Status'), _('Location'), _('Observation'),_('Create Date')],
            'data': elements,
        }
        context['dataTable'] =  dataTable
        return context

class ListStorageinventory(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = CheckinDetail
    template_name = 'historical_storage.html'

    def get_context_data(self, **kwargs):
        context = super(ListStorageinventory, self).get_context_data(**kwargs)
        data = CheckinDetail.objects.all()
        elements = []
        for d in data:
            a=d.supply.stocklevel_set.all().filter(warehouse=d.check_entry.warehouse.id)
            f=''
            if not a:
                f='not in stock'
            else:
                f=a.first().stock
            # print(f)
            elements.append([
                {
                    'type': 'name',
                    'content': d.check_entry.warehouse
                },
                {
                    'type': 'image',
                    'content': d.supply.equipment.image.url
                },
                {
                    'type': 'name',
                    'content': d.check_entry.provider
                },
                {
                    'type': 'label',
                    'content': [{'code': d.check_entry.bill}]
                },
                {
                    'type': 'code_name',
                    'content': {'code':d.check_entry.reason_movement.reason,'name': d.check_entry.reason_movement.movement_text()}
                },
                {
                    'type': 'name',
                    'content': d.check_entry.date_entry
                },
                {
                    'type': 'code_name',
                    'content':{'code':d.supply.size.code,'name':d.supply.size.name}
                },
                {
                    'type': 'name',
                    'content': d.supply.brand
                },
                {
                    'type': 'text',
                    'content': d.supply.material
                },
                {
                    'type': 'name',
                    'content': d.supply.color
                },
                {
                    'type': 'name',
                    'content': d.total 
                },
                {
                    'type': 'name',
                    'content': d.location
                }, 
                {
                    'type': 'name',
                    'content': d.expire_date
                }, 
                {
                     'type': 'name',
                    'content': f            
                }, 
            ])
        dataTable = {
            'card_tittle' : _('Storage Elements'),
            'headers': [_('Warehouse'), _('Supply'), _('Provider'), _('Invoice'), _('Reason'), _('Date'), _('Size'), _('Brand'),_('Material'),_('Color'),_('Total'),_('Location'),_('Expire Date'),_('Storage level')],
            'data': elements,
        }
        context['dataTable'] =  dataTable
        return context

class ReportMatrizPPEforBusinessUnit(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = CheckinDetail
    template_name = 'report_matriz_ppe_for_bu.html'

    def get_context_data(self, **kwargs):
        context = super(ReportMatrizPPEforBusinessUnit, self).get_context_data(**kwargs)
       
        element_protection = Element_Type.objects.get(code='PPE')
        protection_class = element_protection.classification_set.all()
        businesUnit = BusinessUnit.objects.all()
        headers_complex = [] #Complex HEADER

        header_table =[ {
                    'name': _('Business Unit'),
                    'rowspan': "2",
                    'class':'text-center '
                },
               
                {
                    'name': _('Total Positions'),
                    'rowspan': "2",
                    'class':'text-center '
                }]

        for protection in protection_class:
            total = protection.equipment_set.count()
            if total > 0:
               header_table.append(
                    {
                    'name': protection.name,
                    'colspan': total,
                    'class':'text-center '
                    }
                   )
                
        headers_complex.append(header_table) 
        header_table = []        

        for protection in protection_class:
            for equipment in protection.equipment_set.filter(status=True):
                header_table.append(
                      {
                        'name': equipment.name,
                        'class':'text-center '
                      }
                     )

        headers_complex.append(header_table) 
        elements = []
        tr_body_data = []
        for d in businesUnit:
            postions = d.get_postions_structures()  
            tr_body_data.append(
                {
                    'type': 'name',
                    'content': d.name
                }
            )  
            tr_body_data.append( 
                {
                    'type': 'text',
                    'content': d.structure_count()
                }
            )  

            for protection in protection_class:
                for equipment in protection.equipment_set.filter(status=True):
                    total = 0
                    if postions:
                        total = PerPosition.objects.filter(position__in=postions,equipment_id = equipment.id).count()
                    else:
                        total = 0

                    tr_body_data.append(
                       {
                        'type': 'text',
                        'content': total
                       }
                     )             

            elements.append(tr_body_data)
            tr_body_data = []   
        dataTable = {
            'card_tittle' : _('Matrix of personal protection elements'),
            'headers_complex':headers_complex,
            'data': elements,
        }
        context['dataTable'] =  dataTable
        return context

class ReporFrequencyOfChangeEPP(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = Division
    template_name = 'report_frequency_of_change_for_division.html'        

    def get_context_data(self, **kwargs):
        context = super(ReporFrequencyOfChangeEPP, self).get_context_data(**kwargs)

        element_protection = Element_Type.objects.get(code='PPE')
        protection_class = element_protection.classification_set.all()
        divisions = Division.objects.all()
        headers_complex = [] #Complex HEADER

        header_table =[ {
                    'name': _('Division'),                    
                    'class':'text-center '
                },
               
                {
                    'name': _('Total'),
                    'class':'text-center '
                },
                {
                    'name': _('Classication EPP'),
                    'class':'text-center '
                },
                {
                    'name': _('Equipment EPP'),
                    'class':'text-center '
                },
                {
                    'name': _('Total EPP'),
                    'class':'text-center '
                },
                {
                    'name': _('Frequency of Change'),
                    'class':'text-center '
                },
                {
                    'name': _('Annual estimate required'),
                    'class':'text-center '
                },

                ]

                
        headers_complex.append(header_table) 
        header_table = []        

        elements = []
        tr_body_data = []
        for d in divisions:
            postions = d.get_postions_structures()  

            for protection in protection_class:
                for equipment in protection.equipment_set.filter(status=True):
                    total = 0
                    period = 1
                    estimate = 0
                    tr_body_data = []
                    if d.structure_count():
                        if postions:
                            total = PerPosition.objects.filter(position__in=postions,equipment_id = equipment.id).count()      
                                      
                            if equipment.frequency_of_change != 0 and equipment.frequency_of_change != -1 and   equipment.frequency_of_change != 24 :                               
                                period = 12 / equipment.frequency_of_change                               
                                estimate = total * period                                
                            elif equipment.frequency_of_change == 24:                              
                                estimate = total                               
                            elif equipment.frequency_of_change == 0:                               
                                estimate = total
                               
                            elif equipment.frequency_of_change == -1:
                                estimate = total * 240 
                               
                        else:
                            total = 0
                            estimate = 0
                        tr_body_data.append(
                            {
                                'type': 'name',
                                'content': d.name
                            }
                        )  
                        tr_body_data.append( 
                            {
                                'type': 'text',
                                'content': d.structure_count()
                            }
                        )
                        tr_body_data.append( 
                            {
                                'type': 'text',
                                'content':protection.name
                            }
                        ) 
                        tr_body_data.append( 
                            {
                                'type': 'text',
                                'content': equipment.name
                            }
                        ) 
                        tr_body_data.append( 
                            {
                                'type': 'text',
                                'content': total
                            }
                        )
                        tr_body_data.append( 
                            {
                                'type': 'text',
                                'content': equipment.frequency_of_change_text()
                            }
                        ) 
                        tr_body_data.append( 
                            {
                                'type': 'text',
                                'content': int(estimate)
                            }
                        )
                        elements.append(tr_body_data)    

                         
  
        dataTable = {
            'card_tittle' : _('Frequency of Change'),
            'headers_complex':headers_complex,
            'data': elements,
        }
        context['dataTable'] =  dataTable
        return context

class NotificationList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    template_name = 'notifications_list.html'
    model = Notification

    def get_context_data(self, **kwargs):
        context = super(NotificationList, self).get_context_data(**kwargs)
        user = self.request.user
        notification_unread = user.notifications.unread()
        notification_read = user.notifications.read()
        context['notification_unread'] =  notification_unread
        context['notification_read'] =  notification_read
        context['notification_unread_count']  = notification_unread.count 
        context['notification_read_count']  =  notification_read.count
        context['notification_count']  =  user.notifications.count()
        context['user'] = user
        context['notification'] = notification_unread
        return context
