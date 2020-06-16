
from apps.elements.models  import Classification, Element_Type 
from apps.equipments.models import Equipment, Supply
from apps.sizes.models import Area, Size
from apps.requests.models import RequestType
from apps.organizational.models import Position
from apps.publications.models import NewsClass

def get_equipment_select_options(selected_id):
    if selected_id:
        equipment = Equipment.objects.get(id=selected_id)
        equipment_options = [{
            'group':{ 'id':'0','name':equipment.get_element_class_name()},
            'options':[{'id':selected_id,'name':equipment.name,'selected':True}]
        }]
    else: 
        group_class = Classification.objects.all().order_by('name')
        equipment_options = [{
            'group':{ 'id':'0','name':'Classification'},
            'options':[{'id':'','name':'Select Equipment..','disabled':True,'selected':True}]
        }]
        element = []
        for d in group_class:
                element  = d.equipment_set.all()
                equipment_options.append({
                    'group':d,
                    'options':element
                })     
    return   equipment_options 

def get_size_group_area_options(selected_id):
    body_area = Area.objects.all().order_by('name')
    if selected_id:
        size_options = [{
            'group':{ 'id':'0','name':''},
            'options':[{'id':'','name':'Select Size..','selected':False}]
        }]
    else:
        size_options = [{
            'group':{ 'id':'0','name':''},
            'options':[{'id':'','name':'Select Size..','disabled':True,'selected':True}]
        }]

    for b in body_area:
        options= []  
        sizes  = b.size_set.all().order_by('name')
        for s in sizes:
            seleted = False
            if s.id == selected_id:
                seleted = True
            options.append({ 'id': s.id, 'name':s.name, 'selected':seleted})  
        size_options.append({
            'group':{ 'id':b.id ,'name':b.name},
            'options':options
        })
    return   size_options 

def get_supply_select_options():
    group_class = Classification.objects.all().order_by('name')
    equipment_options = [{
        'group':{ id:'0','name':'Default'},
        'options':[{id:'0','name':'Select Supply..'}]
    }]
    element = []
    for d in group_class:
            element  = d.equipment_set.all()
            for e in element:
                supplies = e.supply_set.all()                   
                equipment_options.append({
                    'group':d,
                    'options':supplies
                })     
    return   equipment_options        

def get_element_type_select_options(seleted_id):
    equipment_options = []
    if seleted_id:
        group_class = Element_Type.objects.filter(id=seleted_id)  
    else:    
        group_class = Element_Type.objects.all().order_by('name')
        equipment_options.append( {
            'group':{ id:'0','name':''},
            'options':[{id:'0','name':'Select Type..'}]
        })
    equipment_options.append({
        'group':{ id:'0','name':'Types'},
        'options':group_class
    })
        
    return   equipment_options     

def get_area_select_options(seleted_id):
    area_options = []
    if seleted_id:
        area_data = Area.objects.all().order_by('name')        
        area_data_ops = []
        for e in area_data:
            seleted = False
            if e.id == seleted_id:
                seleted = True
            area_data_ops.append({
                'id':e.id,
                'name':e.name,
                'selected':seleted
            })
        area_options = [{
            'group':{ 'id':'0','name':''},
            'options':area_data_ops
        }]    

        return area_options
    else:    
        area_data = Area.objects.all().order_by('name')
        area_options = [{
            'group':{ id:'0','name':''},
            'options':[{id:'0','name':'Select Body Parts'}]
        }]
    area_options.append({
        'group':{ id:'0','name':'Body Parts'},
        'options':area_data
    })    
    return   area_options   


def get_classification_select_options(seleted_id):
    class_options = []
    if seleted_id:        
        element_data = Element_Type.objects.all().order_by('name')

        for d in element_data:
            class_data  = d.classification_set.all().order_by('name')
            class_data_op = []
            for e in class_data:
                selected = False
                if e.id == seleted_id:
                    selected = True
                class_data_op.append({ 
                    'id':e.id,
                    'name':e.name,
                    'selected':selected
                })
            class_options.append({
                    'group':d,
                    'options':class_data_op
                }) 
        return class_options
    else:    
        element_data = Element_Type.objects.all().order_by('name')

        for d in element_data:
            class_data  = d.classification_set.all().order_by('name')
            class_options.append({
                    'group':d,
                    'options':class_data
                }) 
    return   class_options        

def get_classification_multi_select_options(select_id):
    # print("select_id")
    # print(select_id)
    class_options = []
    if select_id:
        elements = Element_Type.objects.all().order_by('name')
    else:    
        elements = Element_Type.objects.all().order_by('name')
        class_options = [{
            'group':{ id:'0','name':''},
            'options':[{id:'','name':'Select Class..','disabled':True,'selected':True}]
        }]
    for d in elements:
            classification  = d.classification_set.all()
            options= []            
            for e in classification:
                options.append({ 'id': e.id, 'name':e.name, 'selected':find_value_array(select_id,e.id)})                 
        
            class_options.append({'group':d,'options':options}) 
            
    return  class_options 


def get_newsClass_multi_select_options(select_id):
    # print("select_id")
    # print(select_id)
    class_options = []
    options= []  
    if select_id:
        elements = NewsClass.objects.all().order_by('name')
    else:    
        elements = NewsClass.objects.all().order_by('name')       
        
    for e in elements:
        options.append({ 'id': e.id, 'name':e.name, 'selected':find_value_array(select_id,e.id)})                 
        
    class_options.append({'group':[{ 'id':'0','name':'Categories'}],'options':options}) 
            
    return  class_options     

def find_value_array(array=[{ 'id':''}],value=0):
    if array:
        # print("find_value")
        # print(array)
        # print(value)
        for obj in array:
            # print(obj['id'])
            if obj['id'] == value:                
                return True

    return False  

def get_classification_multi_select__for_type_options(type_id):
    class_options = []
    if type_id:
        elements = Element_Type.objects.get(id=type_id)
    else:    
        elements = Element_Type.objects.get(id=type_id) 
    
    classification  = elements.classification_set.all()
    options= []   
    if classification:         
        for e in classification:
            options.append({ 'id': e.id, 'name':e.name, 'selected':False})                 
        
        class_options.append({'group':elements,'options':options})
    else:
        class_options.append({'group':{ 'id':'', 'name':'Not Found'},'options':[ ] })
    return  class_options           


def get_positions_select_options(employee):
    position_options = []
    position = employee.get_position()
    positions = Position.objects.filter(parent_id=position.id)
    position_options.append( {
        'group':{ 'id':'0','name':position.name},
        'options':[{'id':position.id,'name':employee.get_short_name()}]
    })
    if positions:
        position_options.append({
            'group':{ 'id':'0','name':'Subordinate'},
            'options':positions
        })
    return position_options