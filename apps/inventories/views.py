import datetime
import json
from django.shortcuts import render
from django.db import  transaction
from django.views.generic import View, CreateView,UpdateView,DeleteView,ListView, DetailView
from .models import Provider, CheckEntry, ReasonMovement, CheckinDetail, Movement, StockLevel,Supply, Movement,Warehouse,CheckOutPut,CheckOutPutDetail
from apps.requests.models import EmployeeRequest
from apps.assignments.models import Delivered, DeliveredDetail
from apps.requests.models import Status
from .forms import ProviderForms, CheckEntryCreateForms,CheckEntryDetailCreateForms,StockLevelCreateForms
from datetime import datetime, date, time, timedelta
from ippe.util.select_data_util import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Max, Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
# Create your views here.
from notifications.signals import notify
from django.contrib.auth.models import User
from apps.equipments.models import Supply
# from apps.warehouses.models import Warehouse



class ListProvider(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = Provider
    template_name = 'provider_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListProvider, self).get_context_data(**kwargs)
        data = Provider.objects.all()
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
                    'type': 'name',
                    'content': d.NIT
                },
                {
                    'type': 'text',
                    'content': d.Address
                },
                {
                    'type': 'text',
                    'content': d.PhoneNumber
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
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit text-inverse"></i><span class="text-inverse">%s</span>' % _('Edit'), 
                            'href': reverse_lazy("inventories:provider_edit", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash text-inverse"></i><span class="text-inverse" >%s</span>' % _('Delete'), 
                            'href': '#',
                            'pk' : d.id,
                        }
                    ]
                }
            ])
        dataTable = {
            'card_tittle' : 'Provider',
            'headers': ['#', _('Name'), _('NIT'), _('Address'), _('Phone Number'), _('Create Date'), _('Modified Date'), _('Actions')],
            'data': elements,
            'create_button_url' : reverse_lazy("inventories:provider_create"),
            'delete_button_url' : reverse_lazy("inventories:provider_delete")
        }
        context['dataTable'] =  dataTable
        return context



class CreateProvider(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = Provider
    form_class = ProviderForms
    template_name = 'provider_create.html'
    success_url = reverse_lazy('inventories:list_providers')

class UpdateProvider(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model =  Provider
    form_class = ProviderForms    
    template_name = 'provider_create.html'
    success_url = reverse_lazy('inventories:list_providers')

class DeleteProvider(LoginRequiredMixin,DeleteView):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        pk = request.POST['delete_id']
        data = Provider.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('inventories:list_providers'))

class InventoryEntryList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = CheckEntry
    template_name = 'check_entry_list.html'

    def get_context_data(self, **kwargs):
        context = super(InventoryEntryList, self).get_context_data(**kwargs)
        data = CheckEntry.objects.all().order_by('modified_date')
        elements = []
        for d in data:
            
            if d.status == CheckEntry.CODE_PENDING:
                actions =   [
                                {
                                    'content': '<i class="fas fa-lg fa-fw m-r-10 fa-eye text-inverse"></i><span class="text-inverse">%s</span>' % _('Show'), 
                                    'href': reverse_lazy("inventories:inventory_entry_detail_show", kwargs = {'pk': d.id})
                                },
                                {
                                    'content': '<i class="fas fa-lg fa-fw m-r-10 fa-check-square  text-inverse"></i><span class="text-inverse">%s</span>' % _('Confirm Entry'),
                                    'href': reverse_lazy("inventories:inventory_entry_confirm", kwargs = {'pk': d.id})
                                },
                                {
                                    'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit text-inverse"></i><span class="text-inverse">%s</span>' % _('Edit'), 
                                    'href': reverse_lazy("inventories:inventory_entry_detail_create", kwargs = {'pk': d.id})
                                },
                                {
                                    'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash text-inverse"></i><span class="text-inverse" >%s</span>' % _('Delete'), 
                                    'href': '#',
                                    'pk' : d.id,
                                }
                            ]
            else:
                actions =   [
                                {
                                    'content': '<i class="fas fa-lg fa-fw m-r-10 fa-eye text-inverse"></i><span class="text-inverse">%s</span>' % _('Edit'), 
                                    'href': reverse_lazy("inventories:inventory_entry_detail_show", kwargs = {'pk': d.id})
                                }
                            ]

            elements.append([
                {
                    'type': 'code_name',
                    'content': { 'code':('%08d' % int(d.id) ) ,'name':""}
                },
                {
                    'type': 'name',
                    'content': d.warehouse.name
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.provider.NIT,'name':d.provider.name}
                },
                {
                    'type': 'name',
                    'content': d.bill
                },
                {
                    'type': 'code_name',
                    'content': {'code':d.reason_movement.movement_text, 'name':d.reason_movement.reason}
                },
                {
                    'type': 'text',
                    'content': d.date_entry
                },
                {
                    'type': 'text',
                    'content': d.observation
                },
                {
                    'type': 'badge',
                    'content': { 'icon': 'fa fa-dolly-flatbed'  , 'value': d.total_items() ,'href':'#' ,'href':reverse_lazy("inventories:inventory_entry_detail_show", kwargs = {'pk': d.id}  )}
                },
                {
                    'type': 'code_name',
                    'content': {'code':d.storer.position.code, 'name':d.storer.position.name}
                },
                {
                    'type': 'label_statu',
                    'content':{ 'badge':d.status_badge, 'status':d.status_text}
                },
                 {
                    'type': 'badge',
                    'content': { 'icon': 'fa fa-file'  , 'value': d.total_items() ,'target':'top','href':reverse_lazy("inventories:inventory_entry_report", kwargs = {'pk': d.id}  )}
                },
                {
                    'type': 'date',
                    'content': d.create_date 
                },
                 
                {
                    'type': 'action',
                    'actions': actions
                }
            ])
        dataTable = {
            'card_tittle' : _('Inventory Entry'),
            'headers': [_('#Code'), _('Warehouse'),_('Provider'), _('Invoice'),_('Reason'), _('Date'),_('Observation'),_('Items Entry'), _('Storer'),_('Status'),_('Report'), _('Create Date'),  _('Actions')],
            'data': elements,
            'create_button_url' : reverse_lazy("inventories:inventory_entry_create"),
            'delete_button_url' : reverse_lazy("inventories:inventory_entry_delete")
        }
        context['dataTable'] =  dataTable
        return context

class  InventoryEntryCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = CheckEntry
    form_class = CheckEntryCreateForms
    template_name = 'check_entry_create.html'
    #success_url = reverse_lazy('inventories:inventory_entry_list')  

    def get_success_url(self):
        return redirect(reverse_lazy('inventories:inventory_entry_detail_create',  kwargs={'pk': self.object.id }  )   ) 
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect(reverse_lazy('inventories:inventory_entry_detail_create',kwargs={'pk':  post.id } ) )
        else:
            print("Invalid")
        return redirect(reverse_lazy('inventories:inventory_entry_create'   )   )    

class InventoryEntryDetailCreate(LoginRequiredMixin,CreateView):    
    login_url ='authenticate:login'     
    model = CheckinDetail
    form_class = CheckEntryDetailCreateForms
    template_name = 'check_entry_detail_create.html'
    
    def get_success_url(self,**kwargs):
        return  reverse_lazy('inventories:inventory_entry_detail_create' , kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        self.check_entry_pk = self.kwargs['pk']
        context = super(InventoryEntryDetailCreate, self).get_context_data(**kwargs)
        check_entry = CheckEntry.objects.get(id=self.check_entry_pk)
        context['check_entry'] = check_entry        
        context['supply_options'] = get_supply_select_options()
        data = check_entry.checkindetail_set.all()
        elements = []
        for d in data:
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                {
                    'type': 'image',
                    'content': '%s%s' %('../../../media/',d.supply.get_photo())
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.supply.code,'name':d.supply.name}
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.supply.size.code,'name':d.supply.size.name}
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
                    'type': 'text',
                    'content': d.supply.unid_content
                },
                {
                    'type': 'text',
                    'content': d.location
                },
                {
                    'type': 'text',
                    'content': d.warraty_month
                },
                {
                    'type': 'text',
                    'content': d.expire_date
                },
                
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit text-inverse"></i><span class="text-inverse">%s</span>' % _('Edit'), 
                            'href': reverse_lazy("inventories:inventory_entry_detail_update", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash text-inverse"></i><span class="text-inverse" >%s</span>' % _('Delete'), 
                            'href': '#',
                            'pk' : d.id,
                        }
                    ]
                }
            ])
        dataTable = {
            'card_tittle' : _('Supplies Detail'),
            'headers': ['#', _('Photo'),_('Supply'),_('Size'), _('Brand'),_('Material'),_('Color'), _('Total'),_('Content'),_('Location'), _('Warranty'),_('Expire Date'),  _('Actions')],
            'data': elements,
            'create_button_url' :{},
            'delete_button_url' : reverse_lazy("inventories:inventory_entry_detail_delete")
        }
        context['dataTable'] =  dataTable
        return context

class InventoryEntryDetailUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model =  CheckinDetail
    form_class = CheckEntryDetailCreateForms    
    template_name = 'check_entry_detail_update.html'   

    def get_success_url(self,**kwargs):
        return  reverse_lazy('inventories:inventory_entry_detail_create' , kwargs={'pk': self.object.check_entry.id})

    def get_context_data(self, **kwargs):
        self.detail_pk = self.kwargs['pk']
        context = super(InventoryEntryDetailUpdate, self).get_context_data(**kwargs)
        check_detail = CheckinDetail.objects.get(id=self.detail_pk)
        check_entry = check_detail.check_entry
        context['check_entry'] = check_entry
        context['check_detail'] = check_detail
        context['supply_options'] = get_supply_select_options()
        return context

class InventoryEntryDetailDelete(LoginRequiredMixin,DeleteView):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        pk = request.POST['delete_id']
        data = CheckinDetail.objects.get(id = pk)
        pk = data.check_entry.id
        data.delete()
        return redirect(reverse_lazy('inventories:inventory_entry_detail_create', kwargs={'pk': pk }) )  

class InventoryEntryDelete(LoginRequiredMixin,DeleteView):
    def post(self, request, *args, **kwargs):
        pk = request.POST['delete_id']
        data = CheckEntry.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('inventories:inventory_entry_list') )  

class InventoryEntryDetailShow(LoginRequiredMixin,DetailView):
    login_url ='authenticate:login'
    model =  CheckEntry   
    template_name = 'check_entry_detail_show.html' 

    def get_context_data(self, **kwargs):
        self.check_entry_pk = self.kwargs['pk']
        context = super(InventoryEntryDetailShow, self).get_context_data(**kwargs)
        check_entry = CheckEntry.objects.get(id=self.check_entry_pk)
        context['check_entry'] = check_entry
        data = check_entry.checkindetail_set.all()
        elements = []
        for d in data:
            elements.append([
                
                {
                    'type': 'image',
                    'content': '%s%s' %('../../../media/',d.supply.get_photo())
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.supply.code,'name':d.supply.name}
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.supply.size.code,'name':d.supply.size.name}
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
                    'type': 'text',
                    'content': d.supply.unid_content
                },
                {
                    'type': 'text',
                    'content': d.location
                },
                {
                    'type': 'text',
                    'content': d.warraty_month
                },
                {
                    'type': 'text',
                    'content': d.expire_date
                },
                
                
            ])
        dataTable = {
            'card_tittle' : _('Supplies Detail'),
            'headers': [  _('Photo'),_('Supply'),_('Size'), _('Brand'),_('Material'),_('Color'), _('Total'),_('Content'),_('Location in cellar'), _('Warranty'),_('Expire Date')],
            'data': elements,
            'create_button_url' :{},
            'delete_button_url' : reverse_lazy("inventories:inventory_entry_detail_delete")
        }
        context['dataTable'] =  dataTable
        return context        

class InventoryEntryConfirm(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    def get(self, request, *args, **kwargs):
        check_entry = []        
        pk = self.kwargs['pk']
        check_entry = CheckEntry.objects.get(id = pk)
        with transaction.atomic():
            if check_entry:
                warehouse = check_entry.warehouse
                reason     = check_entry.reason_movement                
                for detail in check_entry.checkindetail_set.all():
                    supply     = detail.supply
                    post_inventory = detail.total + detail.supply.get_post_invetary_for_warehouse(warehouse.id)
                    Movement.objects.create(
                        warehouse  = warehouse,
                        supply     = supply,
                        total      = detail.total,
                        post_inventory = post_inventory,
                        location       = detail.location,
                        reason_movement = reason,
                        entry_detail    = detail
                    )    
                    create_entry_stock(supply, post_inventory, warehouse)            
                check_entry.status=check_entry.CODE_COMPLETED
                check_entry.save()              
        return redirect(reverse_lazy('inventories:inventory_entry_list') )
        
def create_entry_stock(supply, total, warehouse):
    stock_level = supply.stocklevel_set.filter(warehouse_id=warehouse.id) 
    if stock_level:
        stock_level = stock_level.latest('id')
        if stock_level:
            stock_level.stock =  total
            stock_level.save()
            return stock_level
    else:
        stock_level = StockLevel.objects.create(
            warehouse = warehouse,
            supply    = supply,
            minimum   = 0,
            maximum   = 0,
            stock     = total            
        )       
        return stock_level

class InventorySupplyList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model =  Supply   
    template_name = 'inventory_supplies_list.html' 

    def get_context_data(self, **kwargs):
        context = super(InventorySupplyList, self).get_context_data(**kwargs)
        warehouse_pk = self.kwargs['warehouse_pk']
        supply_pk = self.kwargs['supply_pk']

        if warehouse_pk != 0 :
            if supply_pk != 0:
                stock_level = StockLevel.objects.filter(warehouse_id=warehouse_pk,supply_id = supply_pk)
            else:
                stock_level = StockLevel.objects.filter(warehouse_id=warehouse_pk) 
        else:
            if supply_pk != 0:
                stock_level = StockLevel.objects.filter(supply_id = supply_pk)
            else:
                stock_level = StockLevel.objects.all()

        warehouse_q = Warehouse.objects.all()
        warehouse = [ {
                'id': 0,
                'name':'All'
        }]
        for p in warehouse_q:
            warehouse.append({ 'id': p.id, 'name':p.name})
        supply_q = Supply.objects.all()    
        supply = [{
                'id': 0,
                'name':'All'
        }]
        for p in supply_q:
            supply.append({ 'id': p.id, 'name':p})

       
        data = stock_level
        elements = []
        for d in data:
            elements.append([               
                {
                    'type': 'name',
                    'content': d.warehouse.name
                },
                {
                    'type': 'image',
                    'content': '%s%s' %('../../../media/',d.supply.get_photo())
                                    
                },
                 {
                    'type': 'label',
                    'content': [{ 'code': d.supply.code}] 
                },
                {
                    'type': 'name',
                    'content': d.supply.name
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.supply.size.code,'name':d.supply.size.name}
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
                    'content': d.stock
                },
                 {
                    'type': 'name',
                    'content': d.minimum
                },
                {
                    'type': 'name',
                    'content': d.maximum
                },
                {
                    'type': 'label_statu',
                    'content':{ 'badge':d.get_level_badge(), 'status':d.get_level_text() }
                },
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit text-inverse"></i><span class="text-inverse">%s</span>' % _('Stock Levels'), 
                            'href': reverse_lazy("inventories:inventory_stock_level_update", kwargs={'pk': d.id})
                        },
                        
                    ]
                }
                
                
            ])
        dataTable = {
            'card_tittle' : _('Stock - Inventory'),
            'headers': [_('Warehouse'),'', _('Code'),_('Supply'),_('Size'), _('Brand'),_('Material'),_('Color'), _( 'Stock'),_('Min'), _('Max'), _('level'),_('Actions')],
            'data': elements,
            'create_button_url' :{},
            'delete_button_url' : {},
            'select_filters':[
                {
                    'id':'warehouse_id',
                    'name':'warehouse',
                    'class_form':'col-md-3 col-md-offset-2',
                    'label':'Warehouse',
                    'selected': warehouse_pk,
                    'options':{ 
                        'values':warehouse,
                    }
                },
                {
                    'id':'supply_id',
                    'name':'supply',
                    'class_form':'col-md-4 col-md-offset-2',
                    'label':'Supply',
                    'selected': supply_pk,
                    'options':{ 
                        'values':supply,
                    }
                }
            ]
        }
        context['dataTable'] =  dataTable
        return context        

class InventoryMovementList(LoginRequiredMixin,ListView):    
    login_url ='authenticate:login'    
    model =  Movement   
    template_name = 'inventory_movement_list.html' 

    def get_context_data(self, **kwargs):
        context = super(InventoryMovementList, self).get_context_data(**kwargs)
        warehouse_pk = self.kwargs['warehouse_pk']
        supply_pk = self.kwargs['supply_pk']
        if warehouse_pk != 0 :
            if supply_pk != 0:
                movement = Movement.objects.filter(warehouse_id=warehouse_pk,supply_id = supply_pk)
            else:
                movement = Movement.objects.filter(warehouse_id=warehouse_pk) 
        else:
            if supply_pk != 0:
                movement = Movement.objects.filter(supply_id = supply_pk)
            else:
                movement = Movement.objects.all()

        context['movement'] = movement
        warehouse_q = Warehouse.objects.all()
        warehouse = [ {
                'id': 0,
                'name':'All'
        }]
        for p in warehouse_q:
            warehouse.append({ 'id': p.id, 'name':p.name})
        supply_q = Supply.objects.all()    
        supply = [{
                'id': 0,
                'name':'All'
        }]
        for p in supply_q:
            supply.append({ 'id': p.id, 'name':p})

        data = movement
        elements = []
        for d in data:
            elements = []
        for d in data:
            elements.append([  
                 {
                    'type': 'code_name',
                    'content': { 'code':d.identifier() }
                },           
                {
                    'type': 'name',
                    'content': d.warehouse
                },
                {
                    'type': 'image',
                    'content': '%s%s' %('../../../media/',d.supply.get_photo())
                                    
                },
                
                {
                    'type': 'code_name',
                    'content': { 'code':d.supply.code,'name':d.supply.name}
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.supply.size.code,'name':d.supply.size.name}
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
                    'type': 'label_statu',
                    'content':{ 'badge':d.reason_movement.type_badge(), 'status':d.reason_movement.movement_text() }
                },
                {
                    'type': 'name',
                    'content': d.reason_movement.reason
                },
                {
                    'type': 'name',
                    'content': d.total
                },
                 {
                    'type': 'name',
                    'content': d.post_inventory
                },
                {
                     'type': 'date',
                    'content': d.create_date 
                },
                
                
                
            ])
        dataTable = {
            'card_tittle' : _('Movements - Inventory'),
            'headers': [_('Identifier'),_('Warehouse'),'',_('Supply'),_('Size'), _('Brand'),_('Material'),_('Color'),_('Type'),_('Reason'), _('Total'), _('Post Total'),_('Created')],
            'data': elements,
            'create_button_url' :{},
            'delete_button_url' : {},
            'select_filters':[
                {
                    'id':'warehouse_id',
                    'name':'warehouse',
                    'class_form':'col-md-3 col-md-offset-2',
                    'label':'Warehouse',
                    'selected': warehouse_pk,
                    'options':{ 
                        'values':warehouse,
                    }
                },
                {
                    'id':'supply_id',
                    'name':'supply',
                    'class_form':'col-md-4 col-md-offset-2',
                    'label':'Supply',
                    'selected': supply_pk,
                    'options':{ 
                        'values':supply,
                    }
                }
            ]
        }
        context['dataTable'] =  dataTable
        return context                

class StockLevelUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = StockLevel
    form_class = StockLevelCreateForms
    template_name = 'stock_level_create.html'
    #success_url = reverse_lazy('inventories:inventory_entry_list')  

    def get_success_url(self):
        return (reverse_lazy('inventories:inventory_supply_list',  kwargs={'warehouse_pk': self.object.warehouse.id,'supply_pk': self.object.supply.id }  )   ) 
    
    def get_context_data(self, **kwargs):
        self.stock_pk = self.kwargs['pk']
        context = super(StockLevelUpdate, self).get_context_data(**kwargs)
        stock = StockLevel.objects.get(id=self.stock_pk)
        supply = stock.supply
        context['stock'] = stock
        context['supply'] = supply
        warehouse = stock.warehouse
        context['warehouse'] = warehouse
        return context

class InventoryOutputList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = CheckOutPut
    template_name = 'check_output_list.html'

    def get_context_data(self, **kwargs):
        context = super(InventoryOutputList, self).get_context_data(**kwargs)
        data = CheckOutPut.objects.filter(~Q(status = 4)).order_by('modified_date')
        elements = []
        for d in data:
            actions =   [
                            {
                                'content': '<i class="fas fa-lg fa-fw m-r-10 fa-luggage-cart text-inverse"></i><span class="text-inverse">%s</span>' % _('Manage'),
                                'href': reverse_lazy("inventories:inventory_output_detail", kwargs = {'pk': d.id})
                            },
                        ]
            if d.date_out:
                text = d.date_out
            else:
                text = "Not dispatched"
            pending_count = "%s / %s" % (d.checkoutputdetail_set.filter(Q(status = CheckOutPut.CODE_DISPATCHED)).count() , d.checkoutputdetail_set.count()) 
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                {
                    'type': 'employee_profile',
                    'content': d.request.employee
                },
                {
                    'type': 'code_name',
                    'content': {'code':d.request.code, 'name':d.request.request_type.name}
                },
                {
                    'type': 'text',
                    'content': d.warehouse.name
                },
                {
                    'type': 'text',
                    'content': d.observation
                },
                {
                    'type': 'code_name',
                    'content': {'code':d.get_reason_movement_text(), 'name':d.get_reason_movement_name()}
                },
                {
                    'type': 'text',
                    'content': text
                },
                {
                    'type': 'label_statu',
                    'content':{ 'badge':d.status_badge, 'status':d.status_text}
                },
                {
                    'type': 'label_statu',
                    'content':{ 'badge':'badge-info', 'status':pending_count}
                },
                {
                    'type': 'date',
                    'content': d.create_date 
                },
                {
                    'type': 'action',
                    'actions': actions
                }
            ])
        dataTable = {
            'card_tittle' : _('Inventory Output'),
            'headers': ['#', _('Employee'), _('Request'), _('Warehouse'),_('Observations'),_('Reason'),_('Out Date'), _('Status'),_('Pending Items'), _('Create Date'),  _('Actions')],
            'data': elements,
            'delete_button_url' : reverse_lazy("inventories:inventory_entry_delete")
        }
        context['dataTable'] =  dataTable
        return context 
        

class InventoryEntryReport(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = CheckEntry
    template_name = 'check_entry_show_doc.html'    

    def get_context_data(self, **kwargs):
        self.pk = self.kwargs['pk']
        context = super(InventoryEntryReport, self).get_context_data(**kwargs)
        entry = CheckEntry.objects.get(id=self.pk)
        entry_detail = entry.checkindetail_set.all()
        context['entry'] = entry
        context['warehouse'] = entry.warehouse
        context['company'] = entry.warehouse.company
        context['entry_detail'] = entry_detail
        return context

class InventoryOutputDetail(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    
    def get(self, request, **kwargs):
        context = {}
        pk = self.kwargs['pk']
        obj = CheckOutPut.objects.get(pk = pk)
        obj_detail = CheckOutPutDetail.objects.filter(check_out_id=pk).order_by('status')
        headers = {
            'output_id' : pk,
            'status_text' : obj.status_text,
            'status_color' : obj.status_badge,
            'employee' : obj.request.employee, 
            'employee_name' : obj.request.employee.get_short_name(),
            'employee_position' : obj.request.employee.structure_set.latest('id').position_name(),
            'employee_gender' : obj.request.employee.get_gender_display(),
            'warehouse' : obj.warehouse,
            'request_date' : obj.request.request_date
        }
        equipments = []
        selected = []
        for equip in obj_detail:
            if(equip.status !=2):
                equipments.append(
                    {
                        'checkout_id' : equip.id,
                        'equipment_url' : equip.equipment.image.url,
                        'equipment_name' : equip.equipment.name,
                        'size' : equip.equipment.area.size_set.latest('id').code,
                        'requested' : equip.total_request,
                        'color' : equip.request_detail.color.name,
                        'supplies' : Supply.objects.filter(equipment_id = equip.equipment.id),
                        'status' : equip.status,
                        'det' : equip
                    },
                )
            else:
                equipments.append(
                    {
                        'equipment_url' : equip.equipment.image.url,
                        'equipment_name' : equip.equipment.name,
                        'size' : equip.equipment.area.size_set.latest('id').code,
                        'requested' : equip.total_request,
                        'color' : equip.request_detail.color.name,
                        'status' : equip.status,
                        'supply_code' : equip.supply.code,
                        'supply_name' : equip.supply.name,
                        'supply_brand' : equip.supply.brand,
                        'total_dispatched' : equip.total_dispatched,
                        'stock' : StockLevel.objects.get(supply_id = equip.supply.id, warehouse_id = obj.warehouse.id).stock
                    }
                )
        #print(equipments)
        context['header'] =  headers
        context['obj_details'] =  equipments
        return render(request, 'check_output_detail.html', context)
    
    def post(self, request, *args, **kwargs):
        obj_detail = CheckOutPutDetail.objects.filter(check_out_id=self.kwargs['pk']).order_by('id')
        obj_out = CheckOutPut.objects.get(pk=self.kwargs['pk'])
        requ = obj_out.request
        detail_count = obj_detail.count()
        counter = 0
        for out_detail in obj_detail:
            if out_detail.status == CheckOutPut.CODE_PENDING: 
                obj_out.status = CheckOutPut.CODE_DELAYED
                obj_out.observation = self.request.POST['observation']
                obj_out.date_out = datetime.now()
                requ.status_request = EmployeeRequest.CODE_DISPACHED_INCOMPLETED
                requ.save()
                obj_out.save()
            else:
                obj_out.observation = self.request.POST['observation']
                obj_out.save()
                counter = counter + 1
        if counter == detail_count:
            obj_out.status = CheckOutPut.CODE_COMPLETED
            obj_out.date_out = datetime.now()
            requ.status_request = EmployeeRequest.CODE_DISPACHED_COMPLETED
            requ.save()
            obj_out.save()
            status = Status.objects.create(
                observation = self.request.POST['observation'],
                status = Status.CODE_DISPACHED_COMPLETED,
                employee_request = obj_out.request,
                employee = request.user.employee,
            )
        else:
            status = Status.objects.create(
                observation = self.request.POST['observation'],
                status = Status.CODE_DISPACHED_INCOMPLETED,
                employee_request = obj_out.request,
                employee = request.user.employee,
            )
        status.save()
        return redirect(reverse_lazy('inventories:inventory_output_list'))

class SupplyAjax(View):

    def post(self, request, *args, **kwargs):
        supply =request.POST.get('id')
        warehouse =request.POST.get('warehouse')
        if supply == '':
            resp = {"response" : "."}
            info = json.dumps(resp)
        else:
            supply = Supply.objects.get(id=supply)
            stock = StockLevel.objects.filter(supply_id=supply,warehouse_id=warehouse) 
            if stock:
                stock = stock.latest('id')               
                supplie = {
                    'supply_code' : supply.code,
                    'supply_name' : supply.name,
                    'supply_brand' : supply.brand.name,
                    'stock' : stock.stock,
                    'stock_flag' : 1
                } 
            else:
                supplie = {
                    'supply_code' : supply.code,
                    'supply_name' : supply.name,
                    'supply_brand' : supply.brand.name,
                    'stock' : 'This supply has not entrances',
                    'stock_flag' : 2
                }          
            info = json.dumps(supplie)
        return HttpResponse(info, content_type='application/json')

class SaveOutput(LoginRequiredMixin,View):
    login_url ='authenticate:login'

    def post(self, request, *args, **kwargs):
        outdetail_id = request.POST.get('pk')
        supply_id = request.POST.get('supp')
        amount = int(request.POST.get('amount'))
        checkout_detail = CheckOutPutDetail.objects.get(id=outdetail_id)
        checkout = CheckOutPut.objects.get(pk = checkout_detail.check_out_id)
        warehouse = checkout.warehouse.id
        stock_level = StockLevel.objects.get(supply_id = supply_id, warehouse_id = warehouse)
        stock_updated = stock_level.stock - amount


        with transaction.atomic():
            checkout_detail.status = CheckOutPut.CODE_DISPATCHED
            checkout_detail.supply = Supply.objects.get(id=supply_id)
            checkout_detail.total_dispatched = amount
            checkout_detail.save()
            stock_level.stock = stock_updated
            stock_level.save()
            movement = Movement.objects.create(
                total = amount,
                post_inventory = stock_updated,
                exit_detail_id = checkout_detail.id,
                reason_movement_id = checkout.reason_movement_id,
                supply_id = supply_id,
                warehouse_id = warehouse
            )
            movement.save()
            delivered = Delivered.objects.filter(checkout_id=checkout_detail.check_out_id)
            if checkout_detail.equipment.frequency_of_change == -1:
                delta = 1
                expire_date = date.today() + timedelta(days = delta)
            elif checkout_detail.equipment.frequency_of_change == 0:
                delta = 2
                expire_date = date.today() + timedelta(days = 365) #Validar  
            else :
                delta = (checkout_detail.equipment.frequency_of_change*30) 
            print(delta)
            if delivered:
                deliver = delivered[0]
                deliver_detail = DeliveredDetail.objects.create(
                    delivered = deliver,
                    movement = movement,
                    supply = checkout_detail.supply,
                    is_accept = 1,
                    expire_date = date.today() + timedelta(days = delta),
                    checkout_detail = checkout_detail
                )
                deliver_detail.save()
            else:
                deliver = Delivered.objects.create(
                    employee = checkout.request.employee,
                    checkout = checkout,
                    deliverer = request.user,
                    status = 1
                )
                deliver.save()
                deliver_detail = DeliveredDetail.objects.create(
                    delivered = deliver,
                    movement = movement,
                    supply = checkout_detail.supply,
                    is_accept = 1,
                    expire_date = date.today() + timedelta(days = delta),
                    checkout_detail = checkout_detail
                )
                deliver_detail.save()
 
            #this is for notify person incharge of warehouse of nevel low!.
            emploee_request = checkout.request.employee
            user_of_request = emploee_request.user_model
            actual_level=stock_level.get_level()
            set_warehouses = checkout.warehouse.storer_set.all()

            if actual_level[0] == StockLevel.CODE_LOW:
                for warehouses_in_charge in set_warehouses:
                    position_warehouse_in_charge = warehouses_in_charge.position
                    person_warehouse_in_charge =  position_warehouse_in_charge.get_ocupate()
                    data_object = {
                        'href' : "inventories:inventory_supply_list", 
                        'warehouse_pk':  warehouse ,
                        'supply_pk':  supply_id
                    }
                    verbo = _("the level for this supply is low")
                    message_type_description = _('the following supply is low at the warehouse')
                    request_type_description = "%s %s" % ( message_type_description,Supply.objects.get(id=supply_id))
                    notify.send(request.user, recipient=person_warehouse_in_charge.user_model , verb=verbo, level='warning',description=request_type_description, target=emploee_request,data=data_object)    
            #end notification


            #this is for notify the employee has been given with new iPPE
            data_object = { 
                'href' : "employees:delivered_detail", 
                'id_ref':  deliver_detail.delivered.id
            }     
            verbo = _("the warehouse has give your new elements")
            message_type_description = _('you have been given with a supply:')
            request_type_description = "%s %s" % ( message_type_description,Supply.objects.get(id = supply_id))
            notify.send(request.user, recipient=user_of_request , verb=verbo, level='warning',description=request_type_description, target=emploee_request,data=data_object)
            #end notification

        return redirect(reverse_lazy("inventories:inventory_output_detail", kwargs = {'pk': checkout.id}) )

class CompletedOutputList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = CheckOutPut
    template_name = 'completed_output_list.html'

    def get_context_data(self, **kwargs):
        context = super(CompletedOutputList, self).get_context_data(**kwargs)
        data = CheckOutPut.objects.filter(status = 4).order_by('modified_date')
        elements = []
        for d in data:
            actions =   [
                             {
                                    'content': '<i class="fas fa-lg fa-fw m-r-10 fa-eye text-inverse"></i><span class="text-inverse">%s</span>' % _('Show'),
                                    'href': reverse_lazy("inventories:inventory_output_completed", kwargs = {'pk': d.id})
                                },
                        ]
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                {
                    'type': 'employee_profile',
                    'content': d.request.employee
                },
                {
                    'type': 'code_name',
                    'content': {'code':d.request.code, 'name':d.request.request_type.name}
                },
                {
                    'type': 'date_short',
                    'content': d.request.create_date
                },
                {
                    'type': 'date_short',
                    'content': d.date_out
                },
                {
                    'type': 'text',
                    'content': d.observation
                },
                {
                    'type': 'label_statu',
                    'content':{ 'badge':d.status_badge, 'status':d.status_text}
                },
                {
                    'type': 'action',
                    'actions': actions
                }
            ])
        dataTable = {
            'card_tittle' : _('Inventory Output'),
            'headers': ['#', _('Employee'), _('Request'), _('Request Date'),_('Managed Date'), _('Observation'),_('Status'),_('Actions')],
            'data': elements,
            'delete_button_url' : reverse_lazy("inventories:inventory_entry_delete")
        }
        context['dataTable'] =  dataTable
        return context 

class CompletedOutputDetail(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    
    def get(self, request, **kwargs):
        context = {}
        pk = self.kwargs['pk']
        obj = CheckOutPut.objects.get(pk = pk)
        obj_detail = CheckOutPutDetail.objects.filter(check_out_id=pk).order_by('status')
        headers = {
            'output_id' : pk,
            'status_text' : obj.status_text,
            'status_color' : obj.status_badge,
            'employee' : obj.request.employee, 
            'employee_name' : obj.request.employee.get_short_name(),
            'employee_position' : obj.request.employee.structure_set.latest('id').position_name(),
            'employee_gender' : obj.request.employee.get_gender_display(),
            'warehouse' : obj.warehouse,
            'request_date' : obj.request.request_date,
            'observation' : obj.observation
        }
        equipments = []
        selected = []
        for equip in obj_detail:
            equipments.append(
                {
                    'equipment_url' : equip.equipment.image.url,
                    'equipment_name' : equip.equipment.name,
                    'size' : equip.equipment.area.size_set.latest('id').code,
                    'requested' : equip.total_request,
                    'color' : equip.request_detail.color.name,
                    'status' : equip.status,
                    'supply_code' : equip.supply.code,
                    'supply_name' : equip.supply.name,
                    'supply_brand' : equip.supply.brand,
                    'total_dispatched' : equip.total_dispatched,
                    'stock' : StockLevel.objects.get(supply_id = equip.supply.id, warehouse_id = obj.warehouse.id).stock
                }
            )
        #print(equipments)
        context['header'] =  headers
        context['obj_details'] =  equipments
        return render(request, 'completed_output_detail.html', context)