import json
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from datetime import date
from django.core import serializers
from decimal import *
from html_json_forms import parse_json_form
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.employees.models import *
from .forms import *
from django.db.models import Avg, Max, Min, Sum
from notifications.signals import notify
# Create your views here.
class InspectionList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = EmployeeInspection
    template_name = 'inspection_list.html'

    def get_queryset(self):
        return EmployeeInspection.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super(InspectionList, self).get_context_data(**kwargs)
        context['form'] = EmployeeInspectionForm()
        data = EmployeeInspection.objects.all()
        user = User.objects.get(username='jalvarezms')
        notification = user.notifications.unread()
        context['user'] = user
        context['notification'] = notification
        
        elements = []
        d = []
        for d in data:
            data_item = []
            data_item = d.employeeinspectiondetail_set.all().order_by('average')[:3]
            detail_items = []
            for item in data_item:                
                detail_items.append({
                        'id':item.id,
                        'name':item.equipment.name,
                        'photo': item.equipment.image.url,
                        'value':("%s %s" % ( int(item.average)   ,'%'))  ,
                        'value_title':item.observation,
                        'class_badge':item.get_class_badge_level_average()
                })
            elements.append([
               
               {
                    'type': 'label',
                    'content': [{ 'code': d.id}]
                },
                {
                    'type': 'employee_profile',
                    'content': d.employee 
                },
                {
                    'type': 'equipment_inspection',
                    'content':detail_items
                },
                
                {
                    'type': 'label_statu',
                    'content': { 'badge':d.get_class_badge_level_average() , 'status': ("%s %s" % (d.qualification,'%'))  }
                },
                {
                    'type': 'text',
                    'content': d.observation 
                },
                {
                    'type': 'date_short',
                    'content': d.inspection_date 
                },
                
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-eye"></i><span >View</span>',
                            'href': reverse_lazy("assignments:inspection_view", kwargs = {'pk': d.id})
                        }
                        
                    ]
                }
            ])
        dataTable = {
            'card_tittle' : 'Inpection Personal',
            'headers': ['Code','Employee','Equipments', 'Calification', 'Observations','Date','Actions'],
            'data': elements,
            'create_button_url' : '#modal-dialog-custom',
            'data_toggle':'modal',
            'delete_button_url' : reverse_lazy("requests:employee_request_detail_delete")
        }
        context['dataTable'] =  dataTable
        return context

class InspectionSelect(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = EmployeeInspection
    template_name = 'inspection_select.html'

    def get_queryset(self):
        return EmployeeInspection.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super(InspectionSelect, self).get_context_data(**kwargs)
        deliv = Delivered.objects.filter(employee = self.request.GET.get('employee'))
        deliv_ids = Delivered.objects.filter(employee = self.request.GET.get('employee')).values('id')
        supply_ids = DeliveredDetail.objects.filter(delivered_id__in = deliv_ids ).values('supply_id')
        delivery_details = DeliveredDetail.objects.filter(delivered_id__in = deliv_ids )
        supplies = Supply.objects.filter(id__in = supply_ids)
        employee = Employee.objects.get(id = self.request.GET.get('employee'))
        
        context['employee'] = employee  
        context['delivery_details'] = delivery_details   
        context['delivered'] = deliv  
        context['supplies'] = supplies
        return context

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return redirect(reverse_lazy('assignments:inspection_list'))
        else:
            employee = Employee.objects.get(id=self.request.GET.get('employee'))
            inspect = request.POST   
            user = User.objects.get(username='jalvarezms')         
            general_observation = request.POST.get('observations')
            form_json = parse_json_form(inspect)             
            employee_inspection_detail = form_json['employee_inspection_detail'][0]
            
            employee_inspection = EmployeeInspection.objects.create(employee=employee,observation=employee_inspection_detail['observation'])
            employee_inspection.save()
            data_object = {
                'href' : "assignments:inspection_view", 
                'id_ref':  employee_inspection.id
            }
            
            if type(employee_inspection_detail['delivery_details']) is list :
                if   type(employee_inspection_detail['delivery_details'][0]) is list :
                    detail_array = employee_inspection_detail['delivery_details'][0]
                else:
                     detail_array = employee_inspection_detail['delivery_details']    

            for index, delivery_detail in enumerate(detail_array):

                if type(employee_inspection_detail['observation_equipment']) is list :
                   observation =  employee_inspection_detail['observation_equipment'][index]
                else:
                   observation =  employee_inspection_detail['observation_equipment']

                if type(employee_inspection_detail['supply']) is list : 
                    supply_id =  employee_inspection_detail['supply'][index]
                else:
                   supply_id =  employee_inspection_detail['supply']  

                if type(employee_inspection_detail['supply']) is list: 
                    equipment_id =  employee_inspection_detail['equipment'][index]
                else:
                   equipment_id =  employee_inspection_detail['equipment']         
                
                delivered_detail = DeliveredDetail.objects.get(id=delivery_detail)
                supply      =   Supply.objects.get(id= supply_id)
                equipment = Equipment.objects.get(id= equipment_id )

                responses = employee_inspection_detail['response']
                detail_inspection = EmployeeInspectionDetail.objects.create(
                        employee_inspection=employee_inspection,
                        delivered_detail=delivered_detail,
                        supply      = supply,
                        equipment =equipment,
                        observation=observation)
                detail_inspection.save()
                   
                for index_item, items in enumerate(employee_inspection_detail['delivery_detail']):
                    is_alert_notify= False
                    text_corrective_action=""
                    print( type(items) )
                    if  type(items) is dict :                        
                        if items['id'] == delivery_detail:
                            if type(items['items']) is str:
                                items =   items['items']
                                items_inspection = ItemsInspection.objects.get(id= items)
                                is_positive = responses[items]
                                is_positive = is_positive['value']
                                response = EmployeeInspectionDetailResponse.objects.create(
                                    items_inspection=items_inspection,
                                    employee_inspection_detail=detail_inspection,
                                    is_positive =is_positive
                                )
                                response.save()
                                print("response.is_positive")
                                print(response.is_positive)
                                print(employee.user)
                                if response.is_positive == False or response.is_positive == 'False':
                                    print("response.is_positive FALSE")
                                    is_alert_notify= True
                                    text_corrective_action = text_corrective_action +' ' + items_inspection.corrective_action
                                    verbo = "%s %s " % ('Corrective Action:  ',detail_inspection.equipment.name)
                                    notify.send(user, recipient=employee.user, verb=verbo,level='warning',description=text_corrective_action, target=employee_inspection,data=data_object)
                                
                            else:    
                                for  response in  items['items']:
                                    items_inspection = ItemsInspection.objects.get(id= response)                                                                    
                                    is_positive = responses[response]
                                    is_positive = is_positive['value']
                                    responser = EmployeeInspectionDetailResponse.objects.create(
                                        items_inspection=items_inspection,
                                        employee_inspection_detail=detail_inspection,
                                        is_positive =is_positive
                                    )
                                    responser.save()
                                    print("responser.is_positive")
                                    print(responser.is_positive)
                                    if  responser.is_positive == False or responser.is_positive == 'False':
                                        print("response.is_positive FALSE")
                                        is_alert_notify= True
                                        text_corrective_action = text_corrective_action +' ' + items_inspection.corrective_action
                                        verbo = "%s %s " % ('Corrective Action:  ',detail_inspection.equipment.name)
                                        notify.send(user, recipient=employee.user, verb=verbo,level='warning',description=text_corrective_action, target=employee_inspection,data=data_object)
                    
                count_detail = detail_inspection.employeeinspectiondetailresponse_set.count()
                print(count_detail)
                count_positivo = detail_inspection.employeeinspectiondetailresponse_set.filter(is_positive=True).count()
                print(count_positivo)
                pondera_detail =   (count_positivo * 100)/count_detail
                print(pondera_detail)
                detail_inspection.average = pondera_detail
                detail_inspection.save()

                

            count_detail = employee_inspection.employeeinspectiondetail_set.count()
            print(count_detail)
            suma_pondera = employee_inspection.employeeinspectiondetail_set.aggregate(Sum('average'))
            print(suma_pondera)
            pondera_total = suma_pondera['average__sum']/count_detail
            print("pondera_total")
            print(pondera_total)
            employee_inspection.qualification=pondera_total
            employee_inspection.save()
            
            verbo = "%s %s %s" % ('PPE inspection results ',int(pondera_total),"%" )
            if pondera_total <= 33:
                notify.send(user, recipient=user, verb=verbo,level='warning',description=employee_inspection.observation, target=employee_inspection,data=data_object)
            elif pondera_total > 33 and pondera_total < 66:
                notify.send(user, recipient=user, verb=verbo,level='info',description=employee_inspection.observation, target=employee_inspection,data=data_object)
            elif pondera_total >= 66 :
                notify.send(user, recipient=user, verb=verbo,level='success',description=employee_inspection.observation, target=employee_inspection,data=data_object)
                
            return redirect(reverse_lazy('assignments:inspection_list'))

class ViewInspection(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = EmployeeInspection
    template_name = 'view_inspection.html'

    def get_queryset(self):
        return EmployeeInspection.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super(ViewInspection, self).get_context_data(**kwargs)
        # print(self.request.GET)
        employee_inspect = EmployeeInspection.objects.get(id=self.kwargs['pk'])
        context['employee_inspect'] = employee_inspect
        inspection_details = EmployeeInspectionDetail.objects.filter(employee_inspection_id = employee_inspect)
        # print(inspection_details)
        context['employee'] = employee_inspect.employee  
        context['inspection_details'] = inspection_details  
        context['delivery_details'] = employee_inspect.employeeinspectiondetail_set.all()   
 
        return context

class DeliveredAjax(View):

    def get(self, request, *args, **kwargs):
        employee_id =request.GET.get('id')
        if employee_id == '':
            resp = {"response" : "."}
            info = json.dumps(resp)
        else:
            emplo =Employee.objects.get(id=employee_id)
            info = {
                'id' : emplo.id,
                'firts_name': emplo.firts_name,
                'last_name': emplo.last_name,
                'position' : emplo.get_postion(),
                'gender' : emplo.gender,
                'photo' : emplo.photo.url,
            }
            info = json.dumps(info)
        return HttpResponse(info, content_type='application/json')
