from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView, View
from django.urls import reverse_lazy
from django.db.models import F
from apps.requests.models import RequestType,EmployeeRequest,DetailRequest,WorkFlowApprovers
from apps.equipments.models import Equipment
from apps.elements.models import Classification
from apps.employees.models import Employee
from apps.requests.forms import RequestTypeForm, EmployeeRequestForm,EmployeeRequestCreateForm,DetailRequestCreateForm,RequestApprovalFlowForm
from django.utils.translation import ugettext_lazy as _


from ippe.util.select_data_util import *
from apps.requests.util.request_util import *
import json
from datetime import date
from datetime import datetime
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from html_json_forms import parse_json_form
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from notifications.signals import notify
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from apps.inventories.models import CheckOutPutDetail


class RequestTypeCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = RequestType
    form_class = RequestTypeForm
    template_name = 'request_type_create.html'

    def get_context_data(self, **kwargs):
        context = super(RequestTypeCreate, self).get_context_data(**kwargs)
        seleted_id = ''
        element_type_options = get_element_type_select_options(seleted_id) 
        context['element_type_options'] = element_type_options
        classification_options = get_classification_multi_select_options(seleted_id)
        context['classification_options'] = classification_options
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        print(data)
        data['element_classification'] = []
        if "cancel" in request.POST:
            return redirect(reverse_lazy('requests:request_type_list'))
        else:
            form = self.form_class(data)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                for ec in request.POST.getlist('element_classification'):
                    post.element_classification.add(ec)
                return redirect(reverse_lazy('requests:request_type_list'))
            else:               
                return redirect(reverse_lazy('requests:request_type_list'))
    
class RequestTypeList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = RequestType
    template_name = 'request_type_list.html'

    def get_queryset(self):
        queryset = RequestType.objects.order_by('id')
        return queryset
    def get_context_data(self, **kwargs):
        context = super(RequestTypeList, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        data = RequestType.objects.all()
        elements = []
        #actions = []
        for d in data:            
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                {
                    'type': 'label',
                    'content': [{ 'code': d.code}] 
                },
                {
                    'type': 'name',
                    'content': d.name
                },
                {
                    'type': 'text',
                    'content': d.detail
                },
                {
                    'type': 'code_name',
                    'content': { 'code': d.element_type.code, 'name': d.element_type.name} 
                },
                {
                    'type': 'label',
                    'content': d.element_classification.all
                    
                },
                 {
                    'type': 'status',
                    'content':d.status
                },
                {
                    'type': 'date',
                    'content': d.create_date
                },
                {
                    'type': 'date',
                    'content': d.modified_date
                },               
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i><span >'+_('Edit')+'</span>',
                            'href': reverse_lazy("requests:request_type_update", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash"></i><span >'+_('Delete')+'</span>',
                            'href': '#',
                            'pk' : d.id,
                        }
                    ]
                }
            ])
        dataTable = {
            'card_tittle' : 'Request Type',
            'headers': ['#', _('Code'),  _('Name'),  _('Description'), _('Element Type'), _('Classification'), _('Status') ,  _('Created date'),  _('Modified date'),   _('Actions')],
            'data': elements,
            'create_button_url' : "create",
            'delete_button_url' : reverse_lazy("requests:request_type_delete")
        }
        context['dataTable'] =  dataTable
        return context   

class RequestTypeUpdate(LoginRequiredMixin,UpdateView):  
    login_url ='authenticate:login'  
    model = RequestType
    form_class = RequestTypeForm    
    template_name = 'request_type_create.html'
    success_url = reverse_lazy('requests:request_type_list')

    def get_context_data(self, **kwargs):
        context = super(RequestTypeUpdate, self).get_context_data(**kwargs)
        request_type = RequestType.objects.get(id=self.kwargs['pk'])
        seleted_id = request_type.element_type_id
        element_type_options = get_element_type_select_options(seleted_id) 
        context['element_type_options'] = element_type_options
        seleted_id = request_type.element_classification.all().values('id')
        classification_options = get_classification_multi_select_options(seleted_id)
        context['classification_options'] = classification_options
        return context

    def post(self, request, *args, **kwargs):
        request_type = RequestType.objects.get(id = self.kwargs['pk'])

        request_type.name= request.POST.get('name')
        request_type.detail=request.POST.get('detail') 
        request_type.status={'on': True , None : False}[request.POST.get('status')] 
        request_type.element_type.id=request.POST.get('element_type') 

        request_type.element_classification.clear() 
        for ec in request.POST.getlist('element_classification'):
                request_type.element_classification.add(ec)

        request_type.save()
        return redirect(reverse_lazy('requests:request_type_list'))

class RequestsTypeDelete(View):     
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        model = RequestType
        pk = request.POST['delete_id']
        data = RequestType.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('requests:request_type_list'))

class EmployeeRequestList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = EmployeeRequest
    template_name = 'request_employee_list.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeeRequestList, self).get_context_data(**kwargs)
        request_type = RequestType.objects.all()
        employee = self.request.user.employee
        context ['requests'] = request_type

        if 'q' in self.request.GET.keys():
            code = int(self.request.GET.get('q'))
            data =self.request.user.employee.employeerequest_set.filter(status_request= code ).order_by(F('create_date').asc())
        else:
            data = employee.employeerequest_set.order_by(F('create_date').asc())

        elements = []
        create_button_url = []
        for ty in request_type:
            create_button_url.append(
                {   
                    'name': ty,
                    'href': '%s' % (reverse_lazy("requests:supplies_request_create", kwargs = {'pk': ty.id})),

                }
            )
        for d in data:
            btn_action =[]
            btn_action.append({
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-eye"></i><span >'+_('Show')+' List</span>',
                            'href': reverse_lazy('requests:employee_request_detail_list', kwargs={'pk': d.id }  )
                        })     
            if d.status_request == EmployeeRequest.CODE_CREATED:
                btn_action.append({
                             'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i><span >'+_('Edit')+'</span>',
                            'href': reverse_lazy('requests:employee_request_detail_create', kwargs={'pk': d.id }  )
                        }) 
                btn_action.append({
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash"></i><span >'+_('Delete')+'</span>',
                            'href': '#',
                            'pk' : d.id,
                        })         
                            

            approvers = []
            for approver in d.get_approver_request_list():
                approvers.append({
                        'id':1,
                        'name':approver.principal_approver.get_ocupate().get_short_name,
                        'photo':approver.principal_approver.get_ocupate().photo.url
                    })      
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                {
                    'type': 'label',
                    'content': [{ 'code': d.code}]
                },
                {
                   'type': 'code_name',
                    'content': { 'code': d.position.code, 'name': d.position.name} 
                },
                {
                    'type': 'code_name',
                    'content': { 'code': d.request_type.code, 'name': d.request_type.name} 
                },
                 {
                    'type': 'text',
                    'content': d.observation  
                },
                {
                    'type': 'text',
                    'content': d.request_date
                },
                
                {
                    'type': 'badge',
                    'content': { 'icon': 'fa fa-archive'  , 'value': d.detailrequest_set.count ,'href': reverse_lazy('requests:employee_request_detail_list', kwargs={'pk': d.id }  ) } 
                },
                {
                    'type': 'approvals',
                    'content': approvers
                }, 
                {
                    'type': 'label_statu',
                    'content':{ 'badge':d.get_level_badge(), 'status':d.status_text() }
                    
                },             
             
                {
                    'type': 'date',
                    'content': d.create_date
                },
                              
                {
                    'type': 'action',
                    'actions': btn_action
                }
            ])
        dataTable = {
            'card_tittle' : _('Requests'),
            'headers': ['#',  _('Code'), _('Position'),  _('Request Type'), _('Observation'),  _('Request Date'), _('Items'),  _('Approvals'), _('Status'), _('Created date') ,   _('Actions')],
            'data': elements,
            'create_button_url' : { 'type':'dropbox' , 'text_btn':'Create Request', 'actions':create_button_url },
            'delete_button_url' : reverse_lazy("requests:employee_request_delete")
        }
        context['dataTable'] =  dataTable
        return context   

class EmployeeRequestCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = EmployeeRequest
    form_class = EmployeeRequestCreateForm
    template_name = 'supplies_request_create.html'
    #success_url = reverse_lazy('requests:supplies_request')

    def get_success_url(self):
        return redirect(reverse_lazy('requests:employee_request_detail_create',  kwargs={'pk': self.object.id }  )   ) 


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeeRequestCreate, self).get_context_data(**kwargs)
        request_type = RequestType.objects.get(id=self.kwargs['pk'])
        context ['requests'] = request_type
        context ['position_options'] =get_positions_select_options(self.request.user.employee)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            request_employee = form.save(commit=False)
           
            employee = request.user.employee
            request_type = request_employee.request_type 
            request_employee_count = employee.employeerequest_set.count()
            request_employee.employee = request_employee.position.get_ocupate()


            request_employee.request_date = date.today()
            request_employee_code = request_code(employee,request_type,request_employee_count  )
            request_employee.code = request_employee_code
            request_employee.save()
            create_status(request_employee,Status.CODE_CREATED, request.user.employee,request_employee.observation )

            #this notify yourself have created a new request
            data_object = {
                'href' : "requests:employee_request_detail_list", 
                'id_ref':  request_employee.id
            }
            user = request.user
            verbo = _("You have created a new request")
            message_type_description = _('You have created a new request of type')
            request_type_description = "%s %s" % ( message_type_description,request_type)
            notify.send(user, recipient=user, verb=verbo, level='success',description=request_type_description, target=request_employee,data=data_object)
            #end notification.
            # print("this for notify yourself")
            
            return redirect(reverse_lazy('requests:employee_request_detail_create',kwargs={'pk':  request_employee.id } ) )
        else:
            print("Invalid")
        return redirect(reverse_lazy('requests:supplies_request_create',  kwargs={'pk':  self.kwargs["pk"] }  )   )    

class EmployeeRequesSenderApproval(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    def get(self, request, *args, **kwargs):              
        pk = self.kwargs['pk']
        emploee_request = EmployeeRequest.objects.get(id = pk)
        if emploee_request:     
            
            #this notify your Boss that you have create a new request and send it for approval
            position = emploee_request.employee.structure_set.latest('id').position.id
            level_approver = emploee_request.next_level_approver
            workflow_Aprovers = get_approver_request(position, emploee_request.request_type_id , level_approver)
            
            postion_principal_approver = workflow_Aprovers.principal_approver
            person_principal_approver = postion_principal_approver.get_ocupate()
            data_object = {
                'href' : "requests:manage_request_show", 
                'id_ref':  emploee_request.id
            }
            First_approval_user = person_principal_approver.user_model
            verbo = _("There is a new request to aprove")
            message_type_description = _('This request is type')
            request_type_description = "%s %s" % ( message_type_description,emploee_request.request_type)
            notify.send(emploee_request.employee.user_model, recipient=First_approval_user, verb=verbo, level='warning',description=request_type_description, target=emploee_request,data=data_object)
            #end notification

            #this notify yourself that you have create a new request and send it for approval
            # print("this is for notify yourself") 
            data_object2 = {
                'href' : "requests:employee_request_detail_list", 
                'id_ref':  emploee_request.id
            }
            user_who_create = emploee_request.employee.user_model
            verbo = _("You have send a new request for approval")
            message_type_description = _('You have send request of type')
            request_type_description = "%s %s" % ( message_type_description,emploee_request.request_type)
            notify.send(user_who_create , recipient=user_who_create , verb=verbo, level='success',description=request_type_description, target=emploee_request,data=data_object2)
            #end notification



            emploee_request.status_request = EmployeeRequest.CODE_APPROVAL_FLOW
            emploee_request.save()
            create_status(emploee_request,Status.CODE_SENDER_APPROVAL_FLOW, emploee_request.employee, 'Sent to approval flow')
            
        
        return redirect(reverse_lazy('requests:supplies_request') )

class EmployeeRequesDetailsCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = DetailRequest
    form_class = DetailRequestCreateForm
    template_name = 'request_detail_create.html'

    def get_success_url(self,**kwargs):
        return  reverse_lazy('requests:employee_request_detail_create' , kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        self.employee_request_pk = self.kwargs['pk']
        context = super(EmployeeRequesDetailsCreate, self).get_context_data(**kwargs)
        employee_request = EmployeeRequest.objects.get(id=self.employee_request_pk)        
                
        context['employee_request'] = employee_request
        context['employee'] = employee_request.employee
        data = employee_request.detailrequest_set.all()
        elements = []
        d = []
        selected_id = ''
        context['equipment_options']  = get_equipment_select_options(selected_id)
        for d in data:            
            elements.append([
               
                {
                    'type': 'image',
                    'content': d.equipment.image.url
                },
                {
                    'type': 'code_name',
                    'content':  { 'code': d.equipment.code, 'name': d.equipment.name} 
                },
                {
                    'type': 'code_name',
                    'content': { 'code': d.assigned_size.size.code, 'name': d.assigned_size.size.name } 
                },
                {
                    'type': 'text',
                    'content': d.total
                },
                {
                    'type': 'text',
                    'content': d.color
                },
                
                {
                    'type': 'date',
                    'content': d.create_date 
                },
                
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i><span >'+_('Edit')+'</span>',
                            'href': reverse_lazy("requests:employee_request_detail_edit", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash"></i><span >'+_('Delete')+'</span>',
                            'href': '#',
                            'pk' : d.id,
                        }
                    ]
                }
            ])
        dataTable = {
            'card_tittle' :  _('Detail Request'),
            'headers': [ _('Photo'), _('Equipment'), _('Size'),  _('Total'),  _('Color'),  _('Create Date'), _('Actions')],
            'data': elements,
            'delete_button_url' : reverse_lazy("requests:employee_request_detail_delete")
        }
        context['dataTable'] =  dataTable
        return context
        
 


class EmployeeRequestDelete(LoginRequiredMixin,DeleteView):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        model = EmployeeRequest
        pk = request.POST['delete_id']
        data = EmployeeRequest.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('requests:supplies_request'))

class EmployeeRequesDetailsUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = DetailRequest
    form_class = DetailRequestCreateForm        
    template_name = 'request_detail_update.html'
    success_url = reverse_lazy('requests:employee_request_detail_create')  

    def get_success_url(self,**kwargs):
        return  reverse_lazy('requests:employee_request_detail_create', kwargs={'pk': self.object.employee_request.id }  )     
   
        
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeeRequesDetailsUpdate, self).get_context_data(**kwargs)
        detailrequest = DetailRequest.objects.get(id=self.kwargs['pk'])
        context ['detail_request'] = detailrequest    
        return context
        

class EmployeeRequesDetailsDelete(LoginRequiredMixin,DeleteView):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        model = DetailRequest
        pk = request.POST['delete_id']
        data = DetailRequest.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('requests:employee_request_detail_create', kwargs={'pk': data.employee_request.id }  ))

class EmployeeRequesDetailsList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = DetailRequest
    template_name = 'request_detail_list.html'
    
    def get_context_data(self, **kwargs):
        self.employee_request_pk = self.kwargs['pk']
        context = super(EmployeeRequesDetailsList, self).get_context_data(**kwargs)
        employee_request = EmployeeRequest.objects.get(id=self.employee_request_pk)
        context['employee_request'] = employee_request
        context['employee'] = employee_request.employee
        data = employee_request.detailrequest_set.all()
        elements = []
        d = []
        for d in data:
            elements.append([
               
                {
                    'type': 'image',
                    'content': d.equipment.image.url
                },
                {
                    'type': 'code_name',
                    'content':   { 'code': d.equipment.code, 'name': d.equipment.name} 
                },
                {
                    'type': 'code_name',
                    'content': { 'code': d.assigned_size.size.code, 'name': d.assigned_size.size.name} 
                },
                {
                    'type': 'text',
                    'content': d.total
                },
                {
                    'type': 'text',
                    'content': d.color
                },
                
                {
                    'type': 'date',
                    'content': d.create_date 
                },
                
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i><span >'+_('Edit')+'</span>',
                            'href': reverse_lazy("requests:employee_request_detail_edit", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash"></i><span >'+_('Delete')+'</span>',
                            'href': '#',
                            'pk' : d.id,
                        }
                    ]
                }
            ])
        dataTable = {
            'card_tittle' :  _('List of Requested Equipment'),
            'headers': [ _('Equipment'), _('Code and Name'), _('Size'),  _('Total'),  _('Color'),  _('Create Date'), _('Actions')],
            'data': elements,
            'delete_button_url' : reverse_lazy("requests:employee_request_detail_delete")
        }
        context['dataTable'] =  dataTable
        return context

class ManageRequestList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = EmployeeRequest
    template_name = 'manage_request_list.html'   
      
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ManageRequestList, self).get_context_data(**kwargs)
        # mostrar solo solicitudes pendiente por el aprobador
        #  data = EmployeeRequest.objects.filter(employee = 4)
        employee = employee = self.request.user.employee
        position = employee.get_position()
        applicant_ids = WorkFlowApprovers.objects.filter(principal_approver = position ).values('applicant_id') 
        print(applicant_ids)
        #supply_ids = DeliveredDetail.objects.filter(delivered_id__in = deliv_ids ).values('supply_id')
        data = EmployeeRequest.objects.filter(position_id__in = applicant_ids).order_by('-status_request')
        elements = []
        for d in data:   
            data_item = []
            data_item = d.detailrequest_set.all()[:3]
            detail_items = []
            for item in data_item:
                detail_items.append({
                        'id':item.id,
                        'name':item.equipment,
                        'photo': item.equipment.image.url
                })
            approvers = []
            for approver in d.get_approver_request_list():
                approvers.append({
                        'id':1,
                        'name':approver.principal_approver.get_ocupate().get_short_name,
                        'photo':approver.principal_approver.get_ocupate().photo.url
                    })     
            elements.append([
                {
                    'type': 'label',
                    'content': [{ 'code': d.code}]
                },
                {
                    'type': 'employee_profile',
                    'content': d.employee 
                },
                
                {
                    'type': 'code_name',
                    'content':   { 'code': d.request_type.code, 'name': d.request_type.name}  
                },
                
               
                {
                    'type': 'text',
                    'content': d.observation  
                },
                {
                    'type': 'approvals',
                    'content':detail_items
                },
                
                {
                   
                    'type': 'approvals',
                    'content': approvers
                
                }, 
                {
                    'type': 'label_statu',
                    'content':{ 'badge':d.get_level_badge, 'status':d.status_text}
                },             
             
                {
                    'type': 'date',
                    'content': d.create_date
                },
                              
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-eye"></i><span >'+_('Show')+' Request</span>',
                            'href': reverse_lazy('requests:manage_request_show', kwargs={'pk': d.id }  )
                        }
                    ]
                }
            ])
        dataTable = {
            'card_tittle' :  _('Manage Approvals Request from the Employee'),
            'headers': [ _('Code'), _('Applicant'),  _('Request'), _('Observation'), _('Items'),  _('Approvals'), _('Status'), _('Created date') ,   _('Actions')],
            'data': elements,
            'create_button_url' : {},
            'delete_button_url' : reverse_lazy("requests:employee_request_delete")
        }
        context['dataTable'] =  dataTable
        return context        

class ManageRequesShow(LoginRequiredMixin,DetailView):
    login_url ='authenticate:login'
    model = EmployeeRequest
    template_name = 'manage_request_show.html'  
    form_class = RequestApprovalFlowForm
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ManageRequesShow, self).get_context_data(**kwargs)
        employee_request = EmployeeRequest.objects.get(id=self.kwargs['pk'])        
        context ['employee_request'] = employee_request
        context ['employee'] = employee_request.employee
        data = employee_request.detailrequest_set.all()
        elements = []
        d = []
        for d in data:
            elements.append([
               
                {
                    'type': 'image',
                    'content': d.equipment.image.url
                },
                {
                    'type': 'text',
                    'content': d.equipment
                },
                {
                    'type': 'text',
                    'content': d.assigned_size
                },
                {
                    'type': 'text',
                    'content': d.total
                },
                {
                    'type': 'text',
                    'content': d.color
                },
                
                {
                    'type': 'date',
                    'content': d.create_date 
                },
                
                # {
                #     'type': 'action',
                #     'actions': [
                #         {
                #             'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i><span >Edit</span>',
                #             'href': reverse_lazy("requests:employee_request_detail_edit", kwargs = {'pk': d.id})
                #         },
                #         {
                #             'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash"></i><span >Delete</span>',
                #             'href': '#',
                #             'pk' : d.id,
                #         }
                #     ]
                # }
            ])
        dataTable = {
            'card_tittle' :  _('Detail Request'),
            'headers': [ _('Equipment'), _('Code and Name'), _('Size'),  _('Total'),  _('Color'),  _('Create Date')],
            'data': elements,
            'delete_button_url' : reverse_lazy("requests:employee_request_detail_delete")
        }
        context['dataTable'] =  dataTable
        return context



class ManageRequesApproval(LoginRequiredMixin,View):  
    login_url ='authenticate:login'  
    def post(self, request, *args, **kwargs):
        status = {}
        pk = self.kwargs['pk']
        pks = self.kwargs['pks']
        observa = request.POST['observa']
        emploee_request = EmployeeRequest.objects.get(id = pk)  
      
        if emploee_request:
            next_level_approver = emploee_request.next_level_approver
            level_max = emploee_request.get_max_level_work_flow() #level__max
            level_max = level_max['level__max']
            type_request = emploee_request.request_type
            approver = get_approver_request(emploee_request.position, type_request, next_level_approver)
            approver_employee =   approver.principal_approver.get_ocupate()
            status = create_status(emploee_request,pks, approver_employee,observa)
           
            if pks == Status.CODE_DECLINED: #en caso de Declinar la solicitud
                emploee_request.status_request = EmployeeRequest.CODE_DECLINED
                emploee_request.save() 

            if  ( (level_max ==  next_level_approver) and ( pks == Status.CODE_APPROVED) ) : #SOLICITUD APROBADA EN NIVEL ULTIMO
                

                emploee_request.status_request = EmployeeRequest.CODE_APPROVAL_COMPLETED
                pks = Status.CODE_APPROVAL_COMPLETED
                emploee_request.save()
                warehouse = get_warehouse(emploee_request.employee)

                if warehouse:
                    create_orden_dispaht(emploee_request, 1,warehouse)
                    status = create_status(emploee_request,Status.CODE_PENDING_DISPATCH, approver_employee,observa)
                                     
                    #notification to warehouse in charge!
                    set_warehouses = warehouse.storer_set.all()
                    detail_req = DetailRequest.objects.filter(employee_request_id=emploee_request.id)
                    checkoutDetail=CheckOutPutDetail.objects.filter(request_detail_id=detail_req[0].id).latest('id')

                    for warehouses_in_charge in set_warehouses:
                        position_warehouse_in_charge = warehouses_in_charge.position
                        person_warehouse_in_charge =  position_warehouse_in_charge.get_ocupate()
                        data_object = {
                            'href' : "inventories:inventory_output_detail", 
                            'id_ref':  checkoutDetail.check_out.id
                        }
                        user_of_request = emploee_request.employee.user_model
                        verbo = _("Your have a new elements to dispatch")
                        message_type_description = _('This request is type')
                        request_type_description = "%s %s" % ( message_type_description,emploee_request.request_type)
                        notify.send(request.user, recipient=person_warehouse_in_charge.user_model , verb=verbo, level='warning',description=request_type_description, target=emploee_request,data=data_object)
                    #end notification

                    #notification to user who made the request that was aproved
                    data_object2 = {
                        'href' : "requests:employee_request_detail_list", 
                        'id_ref':  emploee_request.id
                    }
                    verbo2 = _("your request was approved")
                    notify.send(request.user, recipient=emploee_request.employee.user_model, verb=verbo2 , level='success',description=request_type_description, target=emploee_request,data=data_object2)
                     #end notification

            elif ( (level_max ==  next_level_approver) and ( pks == Status.CODE_DECLINED) ):  #SOLICITUD DENEGADA EN NIVEL ULTIMO

                
                emploee_request.status_request = EmployeeRequest.CODE_DECLINED
                emploee_request.save()

                #notification to request user for notice that his request was declined!
                data_object = {
                    'href' : "requests:employee_request_detail_list", 
                    'id_ref':  emploee_request.id
                }
                user_of_request = emploee_request.employee.user_model
                verbo = _("Your request was deny")
                message_type_description = _('This request is type')
                request_type_description = "%s %s" % ( message_type_description,emploee_request.request_type)
                notify.send(request.user, recipient=user_of_request, verb=verbo, level='warning',description=request_type_description, target=emploee_request,data=data_object)
                 #end notification
            
            if  ( level_max >  next_level_approver):

                emploee_request.next_level_approver  = next_level_approver + 1
                emploee_request.save()

                #notification next level aprovator!
                position = emploee_request.employee.structure_set.latest('id').position.id
                level_approver = emploee_request.next_level_approver
                workflow_Aprovers = emploee_request.get_approver_request(position, emploee_request.request_type_id , level_approver)
                
                postion_principal_approver = workflow_Aprovers.principal_approver
                person_principal_approver = postion_principal_approver.get_ocupate()
                data_object = {
                    'href' : "requests:employee_request_detail_list", 
                    'id_ref':  emploee_request.id
                }
                First_approval_user = person_principal_approver.user_model
                verbo = _("There is a new request to aprove in level ")
                message_type_description = _('This request is type')
                request_type_description = "%s %s" % ( message_type_description,emploee_request.request_type)
                notify.send(emploee_request.employee.user_model, recipient=First_approval_user, verb=verbo, level='warning',description=request_type_description, target=emploee_request,data=data_object)
                #end notification


            
        Datainfo = {'request_id': emploee_request.id ,
                    'status' :'ok'}         
        info = json.dumps(Datainfo)
        return HttpResponse(info, content_type='application/json')
            
         
            

        

