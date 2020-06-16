from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, View,DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from datetime import date
from ippe.util.select_data_util import *
from .models import Element_Type, Classification
from .forms import Element_Type_Form, Element_Classification_Form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
# Create your views here.
class TypeCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = Element_Type
    form_class = Element_Type_Form
    template_name = 'type_create.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect(reverse_lazy('elements:type_list'))
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect(reverse_lazy('elements:type_list'))
            else:
                return redirect(reverse_lazy('elements:type_list'))

class TypeList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = Element_Type
    template_name = 'type_list.html'

    def get_queryset(self):
        return Element_Type.objects.order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super(TypeList, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        data = Element_Type.objects.all()
        elements = []
        actions = []
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
                            'href': reverse_lazy("elements:type_update", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash"></i><span >'+_('Delete')+'</span>',
                            'href': '#',
                            'pk' : d.id,
                        }
                    ]
                }
            ])
        # print(elements)
        dataTable = {
            'card_tittle' : _('Element Type'),
            'headers': ['#', _('Code'), _('Name'), _('Description'), _('Created date'), _('Modified date'),_('Actions')],
            'data': elements,
            'create_button_url' : reverse_lazy("elements:type_create"),
            'delete_button_url' : reverse_lazy("elements:type_delete")
        }
        context['dataTable'] =  dataTable
        return context

class TypeUpdate(LoginRequiredMixin,UpdateView):   
    login_url ='authenticate:login' 
    model = Element_Type
    form_class = Element_Type_Form    
    template_name = 'type_create.html'
    success_url = reverse_lazy('elements:type_list')

class TypeDelete(LoginRequiredMixin,View): 
    login_url ='authenticate:login'    

    def post(self, request, *args, **kwargs):
        model = Element_Type
        pk = request.POST['delete_id']
        data = Element_Type.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('elements:type_list'))

class ClassificationList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = Classification
    template_name = 'classification_list.html'

    def get_queryset(self):
        return Classification.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super(ClassificationList, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        data = Classification.objects.all()
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
                    'type': 'code_name',
                    'content':{ 'code': d.element_type.code, 'name':d.element_type.name}
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
                            'href': reverse_lazy("elements:classification_update", kwargs = {'pk': d.id})
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
            'card_tittle' : _('Element Classification'),
            'headers': ['#', _('Code'), _('Element Type'), _('Name'), _('Description'), _('Status'), _('Created date'), _('Modified date'), _('Actions')],
            'data': elements,
            'create_button_url' : reverse_lazy("elements:classification_create"),
            'delete_button_url' : reverse_lazy("elements:classification_delete")
        }
        context['dataTable'] =  dataTable
        return context

class ClassificationCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = Classification
    template_name = 'classification_form.html'
    form_class = Element_Classification_Form

    def get_context_data(self, **kwargs):
        context = super(ClassificationCreate, self).get_context_data(**kwargs)             
        context['element_type_options'] = get_element_type_select_options(seleted_id='')
        return context
    
    def post(self, request, *args, **kwargs):
        # print(request.POST)
        if "cancel" in request.POST:
            return redirect(reverse_lazy('elements:classification_list'))
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect(reverse_lazy('elements:classification_list'))
            else:
                return redirect(reverse_lazy('elements:classification_list'))

class ClassificationUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = Classification
    template_name = 'classification_form.html'
    success_url = reverse_lazy('elements:classification_list')
    form_class = Element_Classification_Form

    def get_context_data(self, **kwargs):
        context = super(ClassificationUpdate, self).get_context_data(**kwargs)   
        classification_pk = self.kwargs['pk'] 
        classification = Classification.objects.filter(id=classification_pk)
        classification = classification.last()
        context['element_type_options'] = get_element_type_select_options(classification.element_type_id)
        return context

class ClassificationDelete(LoginRequiredMixin,View):
    login_url ='authenticate:login'     

    def post(self, request, *args, **kwargs):
        model = Element_Type
        pk = request.POST['delete_id']
        data = Classification.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('elements:classification_list'))


def select_options_class_for_type(request): 
    type_id = request.GET.get('type_id')
    classifications = get_classification_multi_select__for_type_options(type_id)
    return render(request, 'selects/classification_dropdown_list_options.html', {'classifications': classifications})       