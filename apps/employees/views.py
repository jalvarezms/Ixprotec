import pdfkit
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView,TemplateView,CreateView,UpdateView,DeleteView
from apps.employees.models import Employee
from apps.assignments.models import Delivered, DeliveredDetail
from apps.equipments.models import Supply
from apps.employees.models import AssignedSize
from apps.requests.models import Status
from .forms import Assigned_Size_Form
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from ..sizes.models import Area,Size
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from ippe.util.render_pdf import render_pdf
# Create your views here.
import json
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from ippe.util.select_data_util import *
from django.utils.translation import ugettext as _

class MyDataList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    template_name = 'Profile.html'
    def get_queryset(self,**kwargs):
        return Employee.objects.get(id='1')

    def get_context_data(self , **kwargs):
        context = super(MyDataList,self).get_context_data(**kwargs)
        context['employee'] = self.request.user.employee
        deliv = Delivered.objects.filter(employee = self.request.user.employee.id).values('id')
        # deliver_detail = DeliveredDetail.objects.filter(delivered_id__in = deliv).distinct("supply__name")
        deliver_detail = DeliveredDetail.objects.filter(delivered_id__in = deliv)
        context['deliver_detail'] = deliver_detail
        return context


class RateElement(LoginRequiredMixin,TemplateView):
    login_url ='authenticate:login'
    template_name =  'rate.html'
    def get_context_data(self , **kwargs):
        context = super(RateElement,self).get_context_data(**kwargs)
        context['employee'] = self.request.user.employee
        deliv = Delivered.objects.filter(employee = self.request.user.employee.id)
        deliver_detail = DeliveredDetail.objects.filter(delivered_id__in = deliv)
        id_deliver_item = self.kwargs.get('pk')
        deliver = deliver_detail[int(id_deliver_item)-1]
        context['deliver'] = deliver
        return context


class SizeEmployeeList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    template_name =  'size_list.html'
    model = AssignedSize
    def get_context_data(self , **kwargs):
        context = super(SizeEmployeeList,self).get_context_data(**kwargs)
        # print(self.request.user.employee)
        data = self.request.user.employee.assignedsize_set.all()
        elements = []
        actions = []
        for d in data:
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.size.body_area.code , 'name': d.size.body_area.name  }  
                },
                 {
                    'type': 'text',
                    'content': d.size.body_area.description   
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.size.code ,'name':d.size.name }  
                },
                {
                    'type': 'text',
                    'content': d.size.description   
                },

                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i> <span >'+_('Edit')+'</span>',
                            'href': reverse_lazy("employees:configure_sizes_update", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash"></i> <span >'+_('Delete')+'</span>',
                            'href': '#',
                            'pk' : d.id,
                        }
                    ]
                }
            ])
        dataTable = {
            'card_tittle' : _('Sizes'),
            'headers': ['#',_('Body Area'),_('Description'),_('Size'),_('Size Dimensions'),_('Actions')],
            'data': elements,
            'create_button_url' : reverse_lazy("employees:configure_sizes_create"),
            'delete_button_url' : reverse_lazy("employees:configure_sizes_delete")
        }
        context['dataTable'] =  dataTable
        return context

class SizeEmployeeCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model=AssignedSize
    form_class= Assigned_Size_Form
    template_name= 'size_employee_create.html'
    success_url=reverse_lazy('employees:configure_sizes_list')  
    def get_context_data(self , **kwargs):
        context = super(SizeEmployeeCreate, self).get_context_data(**kwargs)
        context['areaList'] = Area.objects.all()
        context['employee'] = self.request.user.employee
        context['actualSize'] = ""
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            area_id_request = Size.objects.get(id=request.POST.get('size')).body_area_id
            Asigned_sizes_per_employee = AssignedSize.objects.filter(employee_id=request.POST.get('employee'))
            areas_id_per_employee=[]

            for Assigned in Asigned_sizes_per_employee: 
                areas_id_per_employee.append(Assigned.size.body_area_id)

            if area_id_request in areas_id_per_employee:        
                position= areas_id_per_employee.index(area_id_request)
                asigned_id = Asigned_sizes_per_employee[position].id
                AssignedSize.objects.filter(id = asigned_id).update(size_id=request.POST.get('size')) 
                return redirect('employees:configure_sizes_list')

            post.save()
            return redirect('employees:configure_sizes_list')
        # return render(request, "size_employee_create.html", {'form': form})
        return redirect('employees:configure_sizes_create')
    
class SizeEmployeeUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model=AssignedSize
    form_class= Assigned_Size_Form
    template_name='size_employee_update.html'
    success_url=reverse_lazy('employees:configure_sizes_list')
    def get_context_data(self , **kwargs):
        context= super(SizeEmployeeUpdate, self).get_context_data(**kwargs)
        context['areaList'] = Area.objects.all()
        context['sizeid'] = AssignedSize.objects.get(id=self.kwargs.get('pk')).size.id
        context['areaid'] = AssignedSize.objects.get(id=self.kwargs.get('pk')).size.body_area_id
        context['employee'] = self.request.user.employee
        context['actualSize'] =  AssignedSize.objects.get(id=self.kwargs.get('pk'))
        return context

class EquipmentDelete( LoginRequiredMixin,DeleteView):   
    login_url ='authenticate:login'  
    def post(self, request, *args, **kwargs):
        model = AssignedSize
        pk = request.POST['delete_id']
        data = AssignedSize.objects.get(id = pk )
        data.delete()
        return redirect(reverse_lazy('employees:configure_sizes_list'))

class SizeAjax(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    def get(self, request, *args, **kwargs):
        area_id =request.GET.get('id')
        if area_id == '':
            resp = {"response" : "."}
            info = json.dumps(resp)
        else:
            sizelist =Size.objects.filter(body_area_id=area_id)
            jsonList= []
            for size in sizelist:
                jsonList.append(
                {
                    'id' : size.id,
                    'code': size.code,
                    'gender': size.gender_text(),
                    'description' : size.description,
                    'name' : size.name,
                })
            info = json.dumps(jsonList)
        return HttpResponse(info, content_type='application/json')

class DeliveredList(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    def get(self, request, *args, **kwargs):
        context = {}
        if 'q' in self.request.GET.keys():
            code = int(self.request.GET.get('q'))
            data =Delivered.objects.filter(employee_id=request.user.employee.id,checkout_id__isnull=False,status=code)
        else:
            data = Delivered.objects.filter(employee_id=request.user.employee.id,checkout_id__isnull=False)

        # data = Delivered.objects.filter(employee_id=request.user.employee.id,checkout_id__isnull=False)
        elements = []
        actions = []
        for d in data:
            count = "%s / %s" % (d.delivereddetail_set.filter(~Q(is_accept = Delivered.CODE_PENDING)).count() , d.delivereddetail_set.count())
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                {
                    'type': 'label',
                    'content': [{ 'code': d.checkout.request.code}]
                },
                {
                   'type': 'code_name',
                    'content': { 'code': d.checkout.request.request_type.code, 'name': d.checkout.request.request_type.name} 
                },
                {
                    'type': 'text',
                    'content': d.checkout.request.request_date
                },
                {
                    'type': 'text',
                    'content': d.checkout.date_out
                },
                {
                    'type': 'label_statu',
                    'content':{ 'badge':d.checkout.request.get_level_badge, 'status':d.checkout.request.status_text}
                },
                {
                    'type': 'label_statu',
                    'content':{ 'badge':d.checkout.status_badge, 'status':d.checkout.status_text}
                },
                {
                    'type': 'label_statu',
                    'content':{ 'badge':'badge-info', 'status':count}
                },  
                {
                    'type': 'label_statu',
                    'content':{ 'badge':d.get_level_badge, 'status':d.status_text}
                },
                {
                    'type': 'text',
                    'content': d.checkout.observation
                },
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-eye"></i> <span >'+_('Show and Accept')+'</span>',
                            'href': reverse_lazy("employees:delivered_detail", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-print"></i> <span >'+_('Print Delivered Order')+'</span>',
                            'href': reverse_lazy("employees:delivered_pdf", kwargs = {'pk': d.id})
                        },
                    ]
                }
            ])
        dataTable = {
            'card_tittle' : _('Dispatch Supplies'),
            'headers': ['#',_('Request Code'),_('Request Type'),_('Request Date'),_('Managed Date'),_('Request Status'),_('Dispatch Status'),_('Accepted Items'),_('Accepted Status'), _('Dispatch Observations'),_( 'Actions')],
            'data': elements,
        }
        context['dataTable'] =  dataTable
        return render(request, 'delivered_list.html', context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        delivered = Delivered.objects.get(pk=request.POST['delivered_id'])
        delivered.observation = request.POST['observation']
        delivered.save()
        if delivered.status == 1:
            status = Status.objects.create(
                observation = request.POST['observation'],
                status = 11,
                employee_request = delivered.checkout.request,
                employee = request.user.employee,
            )
        elif  delivered.status == 2:
            status = Status.objects.create(
                observation = request.POST['observation'],
                status = 8,
                employee_request = delivered.checkout.request,
                employee = request.user.employee,
            )
        elif  delivered.status == 3:
            status = Status.objects.create(
                observation = request.POST['observation'],
                status = 11,
                employee_request = delivered.checkout.request,
                employee = request.user.employee,
            )
        status.save()
        return redirect(reverse_lazy('employees:delivered_list'))

class DeliveredDetailView(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    def get(self, request, *args, **kwargs):
        context = {}
        requ = Delivered.objects.get(pk=self.kwargs['pk'])
        context['request'] = requ
        return render(request, 'delivered_detail.html', context)

    def post(self, request, *args, **kwargs):
        detail_id = request.POST['detail_id']
        redirect_id = request.POST['delivered_id'] 
        obj = DeliveredDetail.objects.get(pk=detail_id)
        if request.POST['send'] == 'accept':
            obj.is_accept = 2
            obj.observation = request.POST['observation']  
        elif request.POST['send'] == 'refuse':
            obj.is_accept = 3
            obj.observation = request.POST['observation']  
        obj.save()
        delivered = obj.delivered
        delivered_id = delivered.id
        detail_status = DeliveredDetail.objects.filter(delivered=delivered_id)
        count_all = detail_status.count()
        count = 0
        for status in detail_status:
            if status.is_accept != 1:
                count = count + 1
        if count == count_all:
            delivered.status = 2
        else:
            delivered.status = 3
        delivered.save()
        return redirect(reverse_lazy('employees:delivered_detail', kwargs = {'pk': redirect_id}))

class DeliveredPDF(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    
    def get(self, request, *args, **kwargs):
        delivered_id = self.kwargs['pk']
        obj = Delivered.objects.get(pk = delivered_id)
        data = {
            'employee_name' : obj.employee.get_short_name(),
            'position' : obj.employee.get_postion(),
            'area' : obj.employee.get_structure_last().departament.name,
        }
        detail = obj.delivereddetail_set.filter(is_accept=2)
        pdf = render_pdf("detail_pdf.html",{"data": data,'detail':detail})
        return HttpResponse(pdf, content_type="application/pdf")