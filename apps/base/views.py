from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.models import User
from notifications.models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import inspect
import json
from django.utils.translation import ugettext as _
from django.db.models import Q
# Create your views here.

from apps.requests.models import EmployeeRequest,WorkFlowApprovers
from apps.publications.models import Article
from apps.assignments.models import Delivered,DeliveredDetail
from datetime import datetime, timedelta
from apps.employees.models import Employee
from apps.inventories.models import CheckOutPut, StockLevel


class indexViews(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    template_name = 'base.html'
    model = User
    
    #return render(request, 'base.html')

    def get_queryset(self):
        return User.objects.get(username=self.request.user.username)
    def get_context_data(self, **kwargs):
        context = super(indexViews, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        notification = user.notifications.unread()
        context['user'] = user
        context['notification'] = notification
        return context

class NotificationsView(LoginRequiredMixin, View):
    login_url ='authenticate:login'
    model = Notification

    def get(self, request, *args, **kwargs):
        notify = Notification.objects.get(id=self.kwargs['pk'] )
        if notify:
            notify.mark_as_read()
            if notify.data:
                data = notify.data['data']
                if 'warehouse_pk' in data:
                    return redirect(reverse_lazy(data['href'], kwargs = {'warehouse_pk':  data['warehouse_pk'] , 'supply_pk': data['supply_pk'] }))                 
                return redirect(reverse_lazy(data['href'], kwargs = {'pk':  data['id_ref'] }) )
        return redirect(reverse_lazy('reports:notification_list') )        

class Dashboard(LoginRequiredMixin, View):
    login_url ='authenticate:login'

    def get(self,request):
        rows = []
        adminrows = []
        context = {}

        if(request.user.groups.exists()):
            for group in request.user.groups.all():
                if(group.name == 'BASE_USER' or group.name == 'ADMINISTRATOR'):

                    print(_('BASE_USER'))

                    #start a new cards row for request in approval and created and completed
                    cards = []

                    count_request =request.user.employee.employeerequest_set.count()
                    cards.append({'title':_('Total Of My Request'),'url':reverse_lazy('requests:supplies_request'),'time':_('Total'),'count':count_request,'footer':_('Request')})

                    code = EmployeeRequest.CODE_APPROVAL_FLOW
                    count_request_in_aprobal_flow =request.user.employee.employeerequest_set.filter(status_request= code ).count()
                    cards.append({'title': EmployeeRequest.STATUS_CHOICES[code][1],'url':reverse_lazy('requests:supplies_request')+'?q='+str(code),'time':_('Total'),'count':count_request_in_aprobal_flow,'footer':'Request'})

                    code = EmployeeRequest.CODE_APPROVAL_COMPLETED         
                    count_aprobal_completed =request.user.employee.employeerequest_set.filter(status_request= code ).count() 
                    cards.append({'title':EmployeeRequest.STATUS_CHOICES[code ][1],'url':reverse_lazy('requests:supplies_request')+'?q='+str(code),'time':_('Total'),'count':count_aprobal_completed,'footer':'Request'})

                    code = EmployeeRequest.CODE_CREATED 
                    count_aprobal_created =request.user.employee.employeerequest_set.filter(status_request= code ).count()  
                    cards.append({'title':EmployeeRequest.STATUS_CHOICES[code][1],'url':reverse_lazy('requests:supplies_request')+'?q='+str(code),'time':_('Total'),'count':count_aprobal_created,'footer':_('Request')})
                    

                    rows.append({'header': _('Request'), 'cards': cards })
                    adminrows.append({'header': _('Request'), 'cards': cards }) 
                    #end row



                    #start a new cards row for create a new requests this request must
                    cards = []

                    count_ENDW =request.user.employee.employeerequest_set.filter(request_type__code="ENDW").count()
                    cards.append({'title':_('Endownment Request'),'url':reverse_lazy('requests:supplies_request_create', kwargs={'pk': 1 }),'time':_('Total'),'count':count_ENDW,'footer':_(' Request')})
                   
                    count_DRR =request.user.employee.employeerequest_set.filter(request_type__code="DRR").count()
                    cards.append({'title':_('Damage Replacement'),'url':reverse_lazy('requests:supplies_request_create', kwargs={'pk': 4 }),'time':_('Total'),'count':count_DRR,'footer':_('Request')})
                    
                    count_PPE =request.user.employee.employeerequest_set.filter(request_type__code="PPE").count()
                    cards.append({'title':_('Personal Protection'),'url':reverse_lazy('requests:supplies_request_create', kwargs={'pk': 3 }),'time':_('Total'),'count':count_PPE,'footer':_(' Request')})
                    

                    rows.append({'header': _('Create New Request'), 'cards': cards })
                    adminrows.append({'header': _('Create New Request'), 'cards': cards })
                    #end row

                    #start a new cards row for deliveries !!!! fix to show the delivered message in order to have a concordance with the message CODE_PENDING!!!.
                    cards = []

                    count_delivered_Total = Delivered.objects.filter(employee_id= request.user.employee.id,checkout_id__isnull=False).count()
                    cards.append({'title':_('Total Deliveries'),'url':reverse_lazy('employees:delivered_list'),'time':_('Last Week'),'count':count_delivered_Total,'footer':_('Deliveries')})
                    
                    code = Delivered.CODE_PENDING
                    count_delivered_pending = Delivered.objects.filter(employee_id= request.user.employee.id,checkout_id__isnull=False,status=code).count()
                    cards.append({'title':_('Pending For Accept'),'url':reverse_lazy('employees:delivered_list')+'?q='+str(code),'time':_('Last Week'),'count':count_delivered_pending,'footer':_('Deliveries')})
                    
                    code = Delivered.CODE_COMPLETED
                    count_delivered_completed = Delivered.objects.filter(employee_id= request.user.employee.id,checkout_id__isnull=False,status=code).count()
                    cards.append({'title':_('Deliveries Acepted'),'url':reverse_lazy('employees:delivered_list')+'?q='+str(code),'time':_('Last Week'),'count':count_delivered_completed,'footer':_('Deliveries')})
                    

                    rows.append({'header': _('Status Deliveries'), 'cards': cards })
                    adminrows.append({'header': _('Status Deliveries'), 'cards': cards })
                    #end row

                    #start a new cards row for total in deliveries
                    cards = []

                    deliv = Delivered.objects.filter(employee = self.request.user.employee.id).values('id')
                    deliver_detail_Total = DeliveredDetail.objects.filter(delivered_id__in = deliv).count()
                    cards.append({'title':_('Assigned elements'),'url':reverse_lazy('employees:my_data'),'time':_('Total'),'count':deliver_detail_Total,'footer':_('Deliveries')})
                    
                    deliv = Delivered.objects.filter(employee = self.request.user.employee.id).values('id')
                    near_due_date = DeliveredDetail.objects.filter(delivered_id__in = deliv , expire_date__lte = (datetime.now() + timedelta(days=30)), expire_date__gte = datetime.now() ).count()
                    cards.append({'title':_('Near to Due Date'),'url':reverse_lazy('employees:my_data'),'time':_('In Next Month'),'count':near_due_date ,'footer':_('Deliveries')})

                    
                    deliv = Delivered.objects.filter(employee = self.request.user.employee.id).values('id')
                    over_due_date = DeliveredDetail.objects.filter(delivered_id__in = deliv , expire_date__lte = datetime.now(), expire_date__gte=(datetime.now() - timedelta(days=7))).count()
                    cards.append({'title':_('Over to Due Date'),'url':reverse_lazy('employees:my_data'),'time':_('Last Week'),'count':over_due_date,'footer':_('Deliveries')})


                    rows.append({'header': _('Delivers'), 'cards': cards })
                    adminrows.append({'header': _('Delivers'), 'cards': cards })
                    #end row


                    #start a new cards row for publications
                    cards = []
                    count_publications = Article.objects.all().count()
                    cards.append({'title':_('Publications'),'url':reverse_lazy('publications:list_news'),'time':_('Total'),'count': count_publications,'footer':_('Publications')})

                    rows.append({'header': _('New Publications'), 'cards': cards })
                    adminrows.append({'header': _('Create New Request'), 'cards': cards })
                    #end row

                    

                    context['rows'] = rows

                    
                if(group.name == 'MANAGER' or group.name == 'ADMINISTRATOR'):
                    print(_('MANAGER'))


                    # start a new cards row for manage a request 
                    cards = []


                    employee = request.user.employee
                    position = employee.get_position()
                    applicant_ids = WorkFlowApprovers.objects.filter(principal_approver = position ).values('applicant_id') 
                    in_approvalflow_count = EmployeeRequest.objects.filter(position_id__in = applicant_ids, status_request = EmployeeRequest.CODE_APPROVAL_FLOW).count()
                    cards.append({'title':EmployeeRequest.STATUS_CHOICES[EmployeeRequest.CODE_APPROVAL_FLOW][1] ,'url':reverse_lazy('requests:manage_request_list'),'time':'Total','count':in_approvalflow_count,'footer':'Request'})


                    completed_count = EmployeeRequest.objects.filter(position_id__in = applicant_ids, status_request = EmployeeRequest.CODE_APPROVAL_COMPLETED).count()
                    cards.append({'title':EmployeeRequest.STATUS_CHOICES[EmployeeRequest.CODE_APPROVAL_COMPLETED][1] ,'url':reverse_lazy('requests:manage_request_list'),'time':'Last Week','count':completed_count,'footer':'Request'})
                    
                    rows.append({'header': 'Request To Mange', 'cards': cards })
                    adminrows.append({'header': 'Request To Mange', 'cards': cards }) 
                    #end row

                    # start a new cards row for reports
                    cards = []
                                      
                    cards.append({'title':'Items Delivery','url':reverse_lazy('reports:Historic_recibed'),'time':'Last Week','count': -2 ,'footer':'Report'})

                    cards.append({'title':'Request Made','url':reverse_lazy('reports:Historic_request'),'time':'Last Week','count':-2,'footer':'Report'})
          
                    cards.append({'title':'Storage inventory','url':reverse_lazy('reports:Historic_inventory'),'time':'Last Week','count':-2,'footer':'Report'})

                    cards.append({'title':'Matriz PPE for Bussiness Unit','url':reverse_lazy('reports:report_matriz_ppe'),'time':'Last Week','count':-2,'footer':'Report'})

                    cards.append({'title':'Frequency of Change EPP','url':reverse_lazy('reports:report_frequency_change_epp'),'time':'Last Week','count':-2,'footer':'Report'})
                    
                    rows.append({'header': 'Reports', 'cards': cards })
                    adminrows.append({'header': 'Request', 'cards': cards })
                    #end row


                    #start a new cards row for request in approval and created and completed
                    cards = []

                    count_request =request.user.employee.employeerequest_set.count()
                    cards.append({'title':_('Total Of My Request'),'url':reverse_lazy('requests:supplies_request'),'time':_('Total'),'count':count_request,'footer':_('Request')})

                    code = EmployeeRequest.CODE_APPROVAL_FLOW
                    count_request_in_aprobal_flow =request.user.employee.employeerequest_set.filter(status_request= code ).count()
                    cards.append({'title': EmployeeRequest.STATUS_CHOICES[code][1],'url':reverse_lazy('requests:supplies_request')+'?q='+str(code),'time':_('Total'),'count':count_request_in_aprobal_flow,'footer':'Request'})

                    code = EmployeeRequest.CODE_APPROVAL_COMPLETED         
                    count_aprobal_completed =request.user.employee.employeerequest_set.filter(status_request= code ).count() 
                    cards.append({'title':EmployeeRequest.STATUS_CHOICES[code ][1],'url':reverse_lazy('requests:supplies_request')+'?q='+str(code),'time':_('Total'),'count':count_aprobal_completed,'footer':'Request'})

                    code = EmployeeRequest.CODE_CREATED 
                    count_aprobal_created =request.user.employee.employeerequest_set.filter(status_request= code ).count()  
                    cards.append({'title':EmployeeRequest.STATUS_CHOICES[code][1],'url':reverse_lazy('requests:supplies_request')+'?q='+str(code),'time':_('Total'),'count':count_aprobal_created,'footer':_('Request')})
                    

                    rows.append({'header': _('Request'), 'cards': cards })
                    adminrows.append({'header': _('Request'), 'cards': cards }) 
                    #end row



                    #start a new cards row for create a new requests
                    cards = []

                    count_ENDW =request.user.employee.employeerequest_set.filter(request_type__code="ENDW").count()
                    cards.append({'title':_('Endownment Request'),'url':reverse_lazy('requests:supplies_request_create', kwargs={'pk': 1 }),'time':_('Total'),'count':count_ENDW,'footer':_(' Request')})
                   
                    count_DRR =request.user.employee.employeerequest_set.filter(request_type__code="DRR").count()
                    cards.append({'title':_('Damage Replacement'),'url':reverse_lazy('requests:supplies_request_create', kwargs={'pk': 4 }),'time':_('Total'),'count':count_DRR,'footer':_('Request')})
                    
                    count_PPE =request.user.employee.employeerequest_set.filter(request_type__code="PPE").count()
                    cards.append({'title':_('Personal Protection'),'url':reverse_lazy('requests:supplies_request_create', kwargs={'pk': 3 }),'time':_('Total'),'count':count_PPE,'footer':_(' Request')})
                    

                    rows.append({'header': _('Create New Request'), 'cards': cards })
                    
                    #end row

                    #start a new cards row for publications
                    cards = []
                    count_publications = Article.objects.all().count()
                    cards.append({'title':_('Publications'),'url':reverse_lazy('publications:list_news'),'time':_('Last Week'),'count': count_publications,'footer':_('Notification')})

                    rows.append({'header': _('New Publications'), 'cards': cards })
                    #end row


                    context['rows'] = rows

                  
                if(group.name == 'STORER' or group.name == 'ADMINISTRATOR'):
                    print(_('STORER'))
                    # start a new cards row for manage a request 
                    cards = []
                    
                    count_pending_request = CheckOutPut.objects.filter(Q(status=CheckOutPut.CODE_PENDING) | Q(status=CheckOutPut.CODE_DELAYED)).count()
                    cards.append({'title':'Pending Request','url':reverse_lazy('inventories:inventory_output_list'),'time':'Last Week','count':count_pending_request,'footer':'Warehouse Request'})

                    count_completed_request = CheckOutPut.objects.filter(Q(status=CheckOutPut.CODE_COMPLETED) | Q(status=CheckOutPut.CODE_DISPATCHED)).count()
                    cards.append({'title':'Completed Request','url':reverse_lazy('inventories:inventory_output_completed'),'time':'Last Week','count':count_completed_request,'footer':'Warehouse Request'})
                    
                    rows.append({'header': 'Warehouse Request', 'cards': cards })
                    adminrows.append({'header': 'Warehouse Request', 'cards': cards }) 
                    #end row
                    # start a new cards row for manage a request 
                    cards = []
                    
                    count_stock = StockLevel.objects.all() 
                    count_low = 0
                    count_undefined = 0
                    count_optimun = 0
                    count_high = 0
                    for stock in count_stock:
                        if stock.get_level()[0] ==  StockLevel.CODE_UNDEFINED:
                            count_undefined = count_undefined + 1
                        elif stock.get_level()[0] ==  StockLevel.CODE_LOW:
                            count_low = count_low + 1
                        elif stock.get_level()[0] ==  StockLevel.CODE_OPTIMUN:
                            count_optimun = count_optimun + 1
                        elif stock.get_level()[0] ==  StockLevel.CODE_HIGH:
                            count_high = count_high +1
                    cards.append({'title':'Low Level Stock','url':reverse_lazy('inventories:inventory_supply_list', kwargs={'warehouse_pk':'0', 'supply_pk':'0'}),'time':'Last Week','count':count_low,'footer':'Inventories'})
                    cards.append({'title':'Undefined Level Stock','url':reverse_lazy('inventories:inventory_supply_list', kwargs={'warehouse_pk':'0', 'supply_pk':'0'}),'time':'Last Week','count':count_undefined,'footer':'Inventories'})
                    cards.append({'title':'High Level Stock','url':reverse_lazy('inventories:inventory_supply_list', kwargs={'warehouse_pk':'0', 'supply_pk':'0'}),'time':'Last Week','count':count_high,'footer':'Inventories'})
                    cards.append({'title':'Optimum Level Stock','url':reverse_lazy('inventories:inventory_supply_list', kwargs={'warehouse_pk':'0', 'supply_pk':'0'}),'time':'Last Week','count':count_optimun,'footer':'Inventories'})

                    rows.append({'header': 'Inventories', 'cards': cards })
                    adminrows.append({'header': 'Inventories', 'cards': cards }) 
                    #end row
                    context['rows'] = rows

                if(group.name == 'ADMINISTRATOR'):
                    context['rows'] = adminrows
            publications = Article.objects.filter(status =True)
            context['publications'] = publications

        else:
            print( _("this user doesn't have a related group of authentication"))
    
        return render(request,'dashboard.html',context)