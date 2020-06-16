from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, View
from .models import Area, Size
from .forms import AreaForm,SizeForm
from django.urls import reverse_lazy
from ippe.util.select_data_util import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
# Create your views here.


class BodyAreaList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model=Area
    template_name= 'body_area_list.html'
    def get_context_data(self, **kwargs):
        context = super(BodyAreaList, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        data = Area.objects.all()
        elements = []
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
                    'content': d.description
                },
                {
                    'type': 'status',
                    'content': d.status
                },
                {
                    'type': 'date',
                    'content':d.create_date
                },
                {
                    'type': 'date',
                    'content':d.modified_date
                },
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i><span >%s</span>' % _('Edit'),
                            'href': reverse_lazy("sizes:body_area_edit", kwargs = {'pk': d.id})
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
            'card_tittle' : 'Body Area Configuration',
            'headers': ['#', _('Code'), _('Name'),_('Description'), _('Status'), _('Created date'), _('Modified date'), _('Actions')],
            'data': elements,
            'create_button_url' : reverse_lazy("sizes:body_area_create"),
            'delete_button_url' : reverse_lazy("sizes:body_area_delete")
        }
        context['dataTable'] =  dataTable
        return context   

class BodyAreaCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model=Area
    template_name= 'body_area_create.html'
    form_class=AreaForm
    success_url=reverse_lazy('sizes:body_area_list')    
    
class BodyAreaUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model=Area
    form_class=AreaForm
    template_name='body_area_create.html'
    success_url=reverse_lazy('sizes:body_area_list')

class BodyAreaDelete(LoginRequiredMixin,DeleteView):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        model=Area
        # print(request.POST)
        pk = request.POST['delete_id']
        data = Area.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('sizes:body_area_list'))


class SizeList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model=Size
    template_name= 'size_configuration_list.html'

    def get_context_data(self, **kwargs):
        context = super(SizeList, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        data = Size.objects.all()
        elements = []
        
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
                    'content': d.gender_text()
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.body_area.code, 'name':d.body_area.name} 
                },
                {
                    'type': 'name',
                    'content': d.name
                },                
                
                {
                    'type': 'text',
                    'content': d.description
                },
                {
                    'type': 'status',
                    'content':d.status
                },
                {
                    'type': 'date',
                    'content':d.create_date
                },
                {
                    'type': 'date',
                    'content':d.modified_date
                },
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i><span >%s</span>' % _('Edit'),
                            'href': reverse_lazy("sizes:body_size_edit", kwargs = {'pk': d.id})
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
            'card_tittle' : 'Size Configuration',
            'headers': ['#', _('Code'), _('Gender'), _('Body Area'),_('Name'), _('Description'), _('Status'),  _('Create date'),_('Modified date'), _('Actions')],
            'data': elements,
            'create_button_url' : reverse_lazy("sizes:body_size_create"),
            'delete_button_url' : reverse_lazy("sizes:body_size_delete")
        }
        context['dataTable'] =  dataTable
        return context   

class SizeCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model=Size
    template_name= 'size_configuration_create.html'
    form_class=SizeForm
    success_url=reverse_lazy('sizes:body_size_list')

    def get_context_data(self, **kwargs):
        context = super(SizeCreate, self).get_context_data(**kwargs)
        seleted_id = ''
        body_parts_options = get_area_select_options(seleted_id) 
        context['body_parts_options'] = body_parts_options
        return context

class SizeUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model=Size
    form_class=SizeForm
    template_name='size_configuration_create.html'
    success_url=reverse_lazy('sizes:body_size_list')

    def get_context_data(self, **kwargs):
        context = super(SizeUpdate, self).get_context_data(**kwargs)
        size = Size.objects.get(id=self.kwargs['pk'])
        
        seleted_id = size.body_area_id
        body_parts_options = get_area_select_options(seleted_id) 
        # print(body_parts_options)
        context['body_parts_options'] = body_parts_options
        return context


class SizeDelete(LoginRequiredMixin,DeleteView):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        model=Size
        pk = request.POST['delete_id']
        data = Size.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('sizes:body_size_list'))
