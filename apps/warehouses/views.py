from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from .models import Warehouse,Storer
from .forms import WarehouseForm,StorerForm
from django.urls import reverse_lazy
from apps.organizational.models import Position
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
# Create your views here.

class WarehousesCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = Warehouse
    template_name = 'warehouse_create.html'
    form_class=WarehouseForm
    success_url=reverse_lazy('warehouses:warehouse_list')

class WarehousesEdit(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = Warehouse
    template_name = 'warehouse_create.html'
    form_class=WarehouseForm
    success_url=reverse_lazy('warehouses:warehouse_list')

class WarehouseList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = Warehouse
    template_name = 'warehouse_list.html'

    def get_context_data(self, **kwargs):
        context = super(WarehouseList, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        data = Warehouse.objects.all()
        elements = []
        
        for d in data:
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                {
                    'type': 'name',
                    'content': d.name
                },
                {
                    'type': 'text',
                    'content': d.address
                },
                {
                    'type': 'text',
                    'content': d.phone_number
                },
                {
                    'type': 'code_name',
                    'content': { 'code': d.company.code, 'name': d.company.name}   
                },
                {
                    'type': 'code_name',
                    'content': { 'code': d.division.code, 'name': d.division.name}     
                },
                {
                    'type': 'code_name',
                    'content': { 'code': d.departament.code, 'name': d.departament.name}     
                },
                {
                    'type': 'badge',
                    'content': { 'icon': 'fa fa-users'  , 'value': d.storer_set.count ,'href':reverse_lazy("warehouses:add_responsable", kwargs = {'pk': d.id}) } 
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
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-users"></i><span >%s</span>' % _("Add Responsable"),
                            'href': reverse_lazy("warehouses:add_responsable", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i><span >%s</span>' % _('Edit'),
                            'href': reverse_lazy("warehouses:warehouse_edit", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash"></i><span >%s</span>' % _('Delete'),
                            'href': '#',
                            'pk' : d.id,
                        }
                    ]
                }
            ])
        dataTable = {
            'card_tittle' : 'Warehouse',
            'headers': ['#', _('Name'),_('Address'), _('Phone Number'), _('Company'), _('Division'), _('Departament'),_('Responsible'),_('Create Date'),_('Modified Date'),_('Actions')],
            'data': elements,
            'create_button_url' : reverse_lazy("warehouses:warehouse_create"),
            'delete_button_url' : reverse_lazy("warehouses:warehouse_delete")
        }
        context['dataTable'] =  dataTable
        return context

class WarehouseDelete(LoginRequiredMixin,DeleteView):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        model=Warehouse
        pk = request.POST['delete_id']
        data = Warehouse.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('warehouses:warehouse_list'))

class AddResponsable(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = Storer
    template_name = 'add_responsable.html'
    form_class = StorerForm
    def get_success_url(self,**kwargs):
        return  reverse_lazy('warehouses:add_responsable' , kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        self.warehouse_pk = self.kwargs['pk']
        context = super(AddResponsable, self).get_context_data(**kwargs)
        warehouse = Warehouse.objects.get(id=self.warehouse_pk)
        context['warehouse'] = warehouse
        data = warehouse.storer_set.all()
        elements = []
        for d in data:
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                {
                    'type': 'name',
                    'content': d.warehouse
                },
                {
                    'type': 'code_name',
                    'content':  { 'code': d.position.code, 'name': d.position.name}  
                },
                {
                    'type': 'status',
                    'content': d.grand_input
                },
                {
                    'type': 'status',
                    'content': d.grand_output
                },
                {
                    'type': 'status',
                    'content': d.status
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
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i><span >%s</span>' % _('Edit'),
                            'href': reverse_lazy("warehouses:responsable_update", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash"></i><span >%s</span>' % _('Delete'),
                            'href': '#',
                            'pk' : d.id,
                        }
                    ]
                }
            ])
        dataTable = {
            'card_tittle' : ' Stockist',
            'headers': ['#', _('Warehouse'),_('Position'), _('Grand Input'), _('Grand Output'), _('Status'), _('Create Date'),_('Modified Date'),_('Actions')],
            'data': elements,
            'delete_button_url' : reverse_lazy("warehouses:responsable_delete",kwargs = {'pk':warehouse.id})
        }
        context['dataTable'] =  dataTable
        return context

class ResponsableUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'    
    model = Storer
    template_name = 'responsable_update.html'
    form_class=StorerForm

    def get_context_data(self, **kwargs):
        self.storer_pk = self.kwargs['pk']
        context = super(ResponsableUpdate, self).get_context_data(**kwargs)
        storer = Storer.objects.get(id=self.storer_pk)
        context['storer'] = storer
        return context

    def get_success_url(self,**kwargs):
        contex = self.get_context_data()
        return  reverse_lazy('warehouses:add_responsable' , kwargs={'pk': contex['storer'].warehouse.id})

class ResponsableDelete(LoginRequiredMixin,DeleteView):
    login_url ='authenticate:login'
    
    def post(self, request, *args, **kwargs):
        model=Storer
        pk = request.POST['delete_id']
        data = Storer.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('warehouses:add_responsable', kwargs={'pk': self.kwargs['pk']}))