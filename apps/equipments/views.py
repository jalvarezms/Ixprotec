import json
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, View,DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from datetime import date
from django.core import serializers
from django.db.models import Count
from .models import Equipment, Supply, PerPosition,Document,Photo, Video,ItemsInspection
from .forms import Equipment_Form,SupplyForm,PerPositionForm, PerPositionUpdateForm,DocumentsCreateForm,DocumentsUpdateForm,PhotoCreateForm,PhotoUpdateForm, VideoCreateForm, VideoUpdateForm,ItemsInspectionForms
from ippe.util.select_data_util import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
# Create your views here.
class EquipmentCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = Equipment
    form_class = Equipment_Form
    template_name = 'equipment_form.html'

    def get_context_data(self, **kwargs):
        context = super(EquipmentCreate, self).get_context_data(**kwargs)
        seleted_id = ''
        classification_options = get_classification_multi_select_options(seleted_id)
        context['classification_options'] = classification_options
        body_parts_options = get_area_select_options(seleted_id) 
        context['body_parts_options'] = body_parts_options
        context['image_preview'] ='../../../../../static/img/gallery/empty.jpg'
        return context

    def get_success_url(self, **kwargs):
        return (reverse_lazy('equipments:equipment_list'))

class EquipmentList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model : Equipment
    template_name = 'equipment_list.html'

    def get_queryset(self):
        return Equipment.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super(EquipmentList, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        #data = Equipment.objects.all()
        data = Equipment.objects.annotate(num_inspection = Count('itemsinspection' ) )
        elements = []
        actions = []
        for d in data:
            if d.status == True:
                status = _('Activated')
            else:
                status = _('Deactivated')
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                {
                    'type': 'image',
                    'content': d.image.url
                },
                {
                    'type': 'label',
                    'content':[{ 'code': d.code}] 
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
                    'type': 'code_name',
                    'content':  { 'code': d.element_classification.code,'name': d.element_classification.name}
                },
                {
                    'type': 'code_name',
                    'content': { 'code': d.area.code,'name': d.area.name}  
                },
                {
                    'type': 'status',
                    'content':d.status
                },
                {
                    'type': 'text',
                    'content': d.frequency_of_change_text()
                },
                {
                    'type': 'badge',
                    'content': { 'icon': 'fa fa-clipboard-list'  , 'value':d.num_inspection ,'href':reverse_lazy("equipments:equipment_inspetion_items", kwargs = {'pk': d.id}) } #d.required_inspection 
                },
                
                {
                    'type': 'badge',
                    'content': { 'icon': 'fa fa-briefcase'  , 'value': 0 ,'href':'#'}
                },
                {
                    'type': 'badge',
                    'content': { 'icon': 'fa fa-image '  , 'value': 0 , 'href':reverse_lazy("equipments:equipment_img_index", kwargs = {'pk': d.id})} 
                },
                {
                    'type': 'badge',
                    'content':  { 'icon': 'fa fa-file'  , 'value': 0 , 'href':reverse_lazy("equipments:equipment_doc_show", kwargs = {'pk': d.id})} 
                },
                {
                    'type': 'badge',
                    'content':{ 'icon': 'fab fa-youtube'  , 'value':  0 ,'href':reverse_lazy("equipments:equipment_video_show", kwargs = {'pk': d.id})} 
                },
                
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-image fa-lg  fa-fw m-r-10  "> </i> <span >'+_('Images')+'</span>',
                            'href': reverse_lazy("equipments:equipment_img_index", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-file"></i> <span >'+_('Documents')+'</span>',
                            'href': reverse_lazy("equipments:equipment_doc_show", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fab fa-youtube fa-lg fa-fw m-r-10 "> </i><span >'+_('Videos')+'</span>',
                            'href': reverse_lazy("equipments:equipment_video_show", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i><span >'+_('Edit')+'</span>',
                            'href': reverse_lazy("equipments:equipment_update", kwargs = {'pk': d.id})
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
            'card_tittle' : 'Equipment',
            'headers': ['#',_('Equipment'), _('Code'), _('Name'),_('Description'),_('Element Classification'),_('Body Area'),_('Status Active'),_('Frequency of Change'),_('Required Inspection'),_('Assigned'),_('Images'),_('Documents'),_('Videos'),_('Actions')],
            'data': elements,
            'create_button_url' : reverse_lazy("equipments:equipment_create"),
            'delete_button_url' : reverse_lazy("equipments:equipment_delete")
        }
        context['dataTable'] =  dataTable
        return context

class EquipmentUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = Equipment
    template_name = 'equipment_form.html'
    success_url = reverse_lazy('equipments:equipment_list')
    form_class = Equipment_Form

    def get_context_data(self, **kwargs):
            context = super(EquipmentUpdate, self).get_context_data(**kwargs)
            equipment = self.object
            clasification = equipment.element_classification
            seleted_id = clasification.id
            classification_options = get_classification_select_options(seleted_id)
            context['classification_options'] = classification_options
            seleted_id=equipment.area_id
            body_parts_options = get_area_select_options(seleted_id) 
            context['body_parts_options'] = body_parts_options
            
            context['image_preview'] = equipment.image.url
            return context
class EquipmentDelete(LoginRequiredMixin,View):  
    login_url ='authenticate:login'   

    def post(self, request, *args, **kwargs):
        model = Equipment
        pk = request.POST['delete_id']
        data = Equipment.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('equipments:equipment_list'))

class SupplyList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model : Supply
    template_name = 'supplies_list.html'

    def get_queryset(self):
        return Supply.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super(SupplyList, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        data = Supply.objects.all()
        elements = []
        actions = []
        for d in data:
            if d.status == True:
                status = _('Activated')
            else:
                status = _('Deactivated')
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.company.code, 'name':d.company.name}  
                },
                 {
                    'type': 'image',
                    'content': d.equipment.image.url
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
                    'type': 'code_name',
                    'content': { 'code':d.equipment.code, 'name':d.equipment.name}
                },
                {
                    'type': 'name',
                     'content': d.gender_text
                },
                {
                    'type': 'code_name',
                    'content': {'code':d.size.code, 'name':d.size.name}
                },
                {
                    'type': 'text',
                    'content': d.color
                },
                {
                    'type': 'text',
                    'content': d.brand
                },
                {
                    'type': 'text',
                    'content': d.material
                },
                {
                    'type': 'text',
                    'content': d.unid_content
                },
                {
                    'type': 'status',
                    'content':status
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
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i> <span >'+_('Edit')+'</span>',
                            'href': reverse_lazy("equipments:supply_edit", kwargs = {'pk': d.id}) 
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
            'card_tittle' : 'Supplies',
            'headers': ['#',_('Company'),_('Supply'),_('Code'),_('Name'),_('Description'),_('Equipment'),_('Gender'),_('Size'),_('Color'),_('Brand'),_('Material'),_('Unids'),_('Status'),  _('Create date'),_('Modified date'),_('Actions')],
            'data': elements,
            'create_button_url' : reverse_lazy("equipments:supply_create"),
            'delete_button_url' : reverse_lazy("equipments:supply_delete")
        }
        context['dataTable'] =  dataTable
        return context

class AsingEquipmentList(LoginRequiredMixin,View):
    login_url ='authenticate:login'

    def get(self, request, *args, **kwargs):
        position_id =request.GET.get('id')
        if position_id == '':
            resp = {"response" : "."}
            info = json.dumps(resp)
        else:
            perposition = PerPosition.objects.filter(position=position_id)
            # print(perposition)
            per = []
            for perpos in perposition:                
                per.append(
                    {
                        'pos' : position_id,
                        'id' : perpos.id,
                        'position_name' : perpos.position.name,
                        'position_code' : perpos.position.code,
                        'equipment_photo' : perpos.equipment.image.url,
                        'equipment_name' : perpos.equipment.name,
                        'equipment_code' : perpos.equipment.code,
                        'description' : perpos.description,
                        'maximum' : perpos.maximum,
                        'start_date' : perpos.start_date.strftime('%d-%b-%Y'),
                        'end_date' : perpos.end_date.strftime('%d-%b-%Y'),
                        'inspection_period' : perpos.inspection_period
                    },
                )
            # print(per)   
            info = json.dumps(per)
        return HttpResponse(info, content_type='application/json')
        
class PerPositionDelete(LoginRequiredMixin,View):
    login_url ='authenticate:login'

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        position_id = request.POST.get('pos')
        equipment = request.POST.get('id')
        query = PerPosition.objects.get(id=equipment)
        query.delete()

        perposition = PerPosition.objects.filter(position=position_id)
        # print(perposition)
        per = []
        for perpos in perposition:                
            per.append(
                {
                    'pos' : position_id,
                    'id' : perpos.id,
                    'position_name' : perpos.position.name,
                    'position_code' : perpos.position.code,
                    'equipment_photo' : perpos.equipment.image.url,
                    'equipment_name' : perpos.equipment.name,
                    'equipment_code' : perpos.equipment.code,
                    'description' : perpos.description,
                    'maximum' : perpos.maximum,
                    'start_date' : perpos.start_date.strftime('%d-%b-%Y'),
                    'end_date' : perpos.end_date.strftime('%d-%b-%Y'),
                    'inspection_period' : perpos.inspection_period
                },
            )
        # print(per)   
        info = json.dumps(per)
        return HttpResponse(info, content_type='application/json')

class AsignEquipment(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = PerPosition
    form_class = PerPositionForm
    template_name = 'per_position_form.html'

    def get_context_data(self, **kwargs):
            context = super(AsignEquipment, self).get_context_data(**kwargs)
            selected_id = ''
            equip = get_equipment_select_options(selected_id)
            # print(equip)
            context['equipment'] = equip
            return context

class PerPositionSave(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    form_class = PerPositionForm
    
    def post(self, request, *args, **kwargs):
        # print(request.POST.get('position'))
        form = self.form_class(request.POST)
        post = form.save(commit=False)
        post.save()
        position_id=request.POST.get('position')
        perposition = PerPosition.objects.filter(position=position_id)
        # print(perposition)
        per = []
        for perpos in perposition:                
            per.append(
                {
                    'id' : perpos.id,
                    'position_name' : perpos.position.name,
                    'position_code' : perpos.position.code,
                    'equipment_photo' : perpos.equipment.image.url,
                    'equipment_name' : perpos.equipment.name,
                    'equipment_code' : perpos.equipment.code,
                    'description' : perpos.description,
                    'maximum' : perpos.maximum,
                    'start_date' : perpos.start_date.strftime('%d-%b-%Y'),
                    'end_date' : perpos.end_date.strftime('%d-%b-%Y'),
                    'inspection_period' : perpos.inspection_period
                },
            )
        # print(per)   
        info = json.dumps(per)
        return HttpResponse(info, content_type='application/json')

class PerpositionUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = PerPosition
    template_name = 'per_position_update.html'
    success_url = reverse_lazy('equipments:perposition_create')
    form_class = PerPositionUpdateForm

    def get_success_url(self, **kwargs):
        if 'val' in self.request.GET:
            url = reverse_lazy('equipments:perposition_create')
        else:
            url = reverse_lazy('equipments:perposition_list')
        return url
                    
class SupplieCreateView(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = Supply
    form_class = SupplyForm
    template_name = 'supplies_form.html'
    success_url = reverse_lazy('equipments:supply_list')

    def get_context_data(self, **kwargs):
        context = super(SupplieCreateView, self).get_context_data(**kwargs)
        selected_id = ''
        context['equipment_options']  = get_equipment_select_options(selected_id)
        context['size_options']  = get_size_group_area_options(selected_id)
        return context

class SupplyUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = Supply
    form_class = SupplyForm    
    template_name = 'supplies_update.html'
    success_url = reverse_lazy('equipments:supply_list')
    def get_context_data(self, **kwargs):
        context = super(SupplyUpdate, self).get_context_data(**kwargs)
        selected_id = self.object.equipment_id
        context['equipment_options']  = get_equipment_select_options(selected_id)
        context['size_options']  = get_size_group_area_options(self.object.size_id)
        return context

class SupplyDelete(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        model = Supply
        pk = request.POST['delete_id']
        data = Supply.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('equipments:supply_list'))

class PerPositionList(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model : Equipment
    template_name = 'per_position_list.html'

    def get_queryset(self):
        return Equipment.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super(PerPositionList, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        data = PerPosition.objects.all()
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
                    'content': { 'code':d.position.code, 'name':d.position.name}
                },
                {
                    'type': 'code_name',
                    'content': { 'code':d.equipment.code, 'name':d.equipment.name}
                },
                {
                    'type': 'text',
                    'content': d.description
                },
                {
                    'type': 'text',
                    'content': d.maximum
                },
                {
                    'type': 'date',
                    'content': d.start_date
                },
                {
                    'type': 'date',
                    'content': d.end_date
                },
                {
                    'type': 'text',
                    'content': d.inspection_period
                },
                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i> <span >'+_('Edit')+'</span>',
                            'href': reverse_lazy("equipments:perposition_update", kwargs = {'pk': d.id})
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
            'card_tittle' : 'Equipment Per Position',
            'headers': ['#',_('Position'),_('Equipment'),_('Description'),_('Max Permited'),_('Start Date'),_('End Date'),_('Inspection Period'),_('Actions')],
            'data': elements,
            'create_button_url' : reverse_lazy("equipments:perposition_create"),
            'delete_button_url' : reverse_lazy("equipments:perposition_delete")
        }
        context['dataTable'] =  dataTable
        return context

class EquipmentDocShow(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = Equipment
    template_name = 'equipment_documents_show.html'
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         equipments = Equipment.objects.get(id=self.kwargs['pk'])       
         context['equipments'] = equipments
         return context

class EquipmentDocCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = Document
    form_class = DocumentsCreateForm
    template_name = 'equipment_documents_create.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipments = Equipment.objects.get(id=self.kwargs['equipment'])       
        context['equipments'] = equipments
        return context

    def get_success_url(self,**kwargs):
        return reverse_lazy('equipments:equipment_doc_show' ,  kwargs={'pk':  self.kwargs['equipment'] }  )  
    
    
class EquipmentDocEdit(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = Document
    form_class = DocumentsUpdateForm
    template_name = 'equipment_documents_update.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         document = Document.objects.get(id=self.kwargs['pk'])       
         context['equipments'] = document.equipment_by
         return context

    def get_success_url(self,**kwargs):
        contex = self.get_context_data()
        return reverse_lazy('equipments:equipment_doc_show' ,  kwargs={'pk':  contex['equipments'].id }  )  

class EquipmentDocDelete(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        model = Document
        pk = request.POST['delete_id']
        data = Document.objects.get(id = pk)
        equipment_id = data.equipment_by.id
        data.delete()
        return redirect(reverse_lazy('equipments:equipment_doc_show',  kwargs={'pk':  equipment_id }  )   )  

class EquipmentVideoDelete(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        model = Video
        pk = request.POST['delete_id']
        data = Video.objects.get(id = pk)
        equipment_id = data.equipment_by.id
        data.delete()
        return redirect(reverse_lazy('equipments:equipment_video_show',  kwargs={'pk':  equipment_id }  )   )           

class EquipmentImgCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = Photo
    form_class = PhotoCreateForm
    template_name = 'equipment_img_create.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipments = Equipment.objects.get(id=self.kwargs['equipment'])       
        context['equipments'] = equipments
        return context

    def get_success_url(self,**kwargs):
        return reverse_lazy('equipments:equipment_img_index' ,  kwargs={'pk':  self.kwargs['equipment'] }  )  
    
class EquipmentImgIndex(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    model = Photo
    template_name = 'equipment_img_show.html'
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         equipments = Equipment.objects.get(id=self.kwargs['pk'])       
         context['equipments'] = equipments
         return context

class EquipmentImgEdit(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = Photo
    form_class = DocumentsUpdateForm
    template_name = 'equipment_img_update.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         photo = Photo.objects.get(id=self.kwargs['pk'])       
         context['equipments'] = photo.equipment_by
         return context

    def get_success_url(self,**kwargs):
        contex = self.get_context_data()
        return reverse_lazy('equipments:equipment_img_index' ,  kwargs={'pk':  contex['equipments'].id }  )             
    
class EquipmentImgDelete(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        model = Photo
        pk = request.POST['delete_id']
        data = Photo.objects.get(id = pk)
        equipment_id = data.equipment_by.id
        data.delete()
        return redirect(reverse_lazy('equipments:equipment_img_index',  kwargs={'pk':  equipment_id }  )   )    

class EquipmentGetJx(View):

    def get(self, request, *args, **kwargs):
        print(request.GET)
        equipment_id =request.GET.get('id')
        info=[]
        if equipment_id == '':
            resp = {"response" : "."}
            info = json.dumps(resp)
        else:
            equipment = Equipment.objects.get(id=equipment_id)
            Datainfo = {
                'name':equipment.name,
                'code':equipment.code,
                'description':equipment.description,
                'area':equipment.area.name,
                'time_of_life':equipment.frequency_of_change_text(),
                'image':equipment.image.url,
                'status':equipment.status,
                'type':equipment.get_element_type_name(),
                'class':equipment.get_element_class_name()
            }
            info = json.dumps(Datainfo)
        return HttpResponse(info, content_type='application/json')

class EquipmentVideoShow(LoginRequiredMixin,DetailView):
    login_url ='authenticate:login'
    model = Equipment
    template_name = 'equipment_video_show.html'
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         equipments = Equipment.objects.get(id=self.kwargs['pk'])       
         context['equipments'] = equipments
         return context

class EquipmentVideoCreate(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = Video
    form_class = VideoCreateForm
    template_name = 'equipment_video_create.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipments = Equipment.objects.get(id=self.kwargs['equipment'])       
        context['equipments'] = equipments
        return context

    def get_success_url(self,**kwargs):
        return reverse_lazy('equipments:equipment_video_show' ,  kwargs={'pk':  self.kwargs['equipment'] }  )  
    
class EquipmentVideoEdit(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = Video
    form_class = VideoUpdateForm
    template_name = 'equipment_video_update.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         video = Video.objects.get(id=self.kwargs['pk'])       
         context['equipments'] = video.equipment_by
         return context

    def get_success_url(self,**kwargs):
        contex = self.get_context_data()
        return reverse_lazy('equipments:equipment_video_show' ,  kwargs={'pk':  contex['equipments'].id }  )          

class SupplyGetJx(View):    
    def get(self, request, *args, **kwargs):
        supply_id =request.GET.get('id')
        if supply_id == '':
            resp = {"response" : "."}
            info = json.dumps(resp)
        else:
            supply = Supply.objects.select_related('equipment').get(id=supply_id)
            Datainfo = {
                'name':supply.name,
                'brand':supply.brand.name,
                'material':supply.material,
                'size':supply.size.name,
                'color':supply.color.name,
                'units':supply.unid_content,
                'Source_URL':supply.equipment.image.url
            }  
            info = json.dumps(Datainfo)
        return HttpResponse(info, content_type='application/json')

class EquipmentInspetionItem(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = ItemsInspection
    form_class = ItemsInspectionForms
    template_name = 'equipment_inspection_items_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipments = Equipment.objects.get(id=self.kwargs['pk'])       
        context['equipments'] = equipments
        return context

    def get_success_url(self,**kwargs):
        contex = self.get_context_data()
        return reverse_lazy('equipments:equipment_inspetion_items' ,  kwargs={'pk':  contex['equipments'].id }  )     

class EquipmentInspetionItemDelete(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        model = ItemsInspection
        pk = request.POST['delete_id']
        data = ItemsInspection.objects.get(id = pk)
        equipment_id = data.equipment.id
        data.delete()
        return redirect(reverse_lazy('equipments:equipment_inspetion_items',  kwargs={'pk':  equipment_id }  )   )    


class EquipmentInspetionItemUpdate(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = ItemsInspection
    form_class = ItemsInspectionForms
    template_name = 'equipment_inspection_items_create.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         data = ItemsInspection.objects.get(id=self.kwargs['pk'])       
         context['equipments'] = data.equipment
         return context

    def get_success_url(self,**kwargs):
        contex = self.get_context_data()
        return reverse_lazy('equipments:equipment_inspetion_items' ,  kwargs={'pk':  contex['equipments'].id }  )          