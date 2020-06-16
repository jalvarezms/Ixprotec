from apps.employees.models import Employee,AssignedSize
from apps.sizes.models import Size
from django.utils.translation import ugettext_lazy as _
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
def employee_response():
    return { 'id':'', 'code':'', 'short_name':'','codeResponse':'','messageResponse':'Ok' } 

def employee_sync(data, response):
    code = data['code']
    response['code'] = data['code']
    response['short_name'] = data['short_name']   
    try:
        if code is not None:
            employee = Employee.objects.get(code=code)
    except:
        response['codeResponse']= HTTP_400_BAD_REQUEST 
        response['messageResponse']= _("code is null")     
    create_flag = None
    update_flag = None 
    try:
        if data['sizes']:
            try:
                obj= Employee.objects.get(code=data['code'])
                obj.code = data['code']
                obj.firts_name = data['firts_name']
                obj.second_name = data['second_name']
                obj.short_name = data['short_name']
                obj.gender = data['gender']
                obj.document = data['document']
                obj.number_doc = data['number_doc']
                set_sizes = set({})
                set_data_sizes = set(data['sizes'])
                for size in obj.assignedsize_set.all():
                    set_sizes.add(size.size.code)
                data_difference = set_data_sizes.difference(set_sizes)
                actual_difference = set_sizes.difference(set_data_sizes)
                intersection_set = set_sizes.intersection(set_data_sizes)
                if data_difference:
                    for update_sizes in data_difference:
                        intersection_set.add(str(update_sizes))
                for size_code in intersection_set:
                    try: 
                        size = Size.objects.get(code = size_code)
                    except:
                        size = Size.objects.get(code = size_code, gender=obj.gender)
                    obj.sizes.add(size)
                for remove_size in actual_difference:
                    try: 
                        size = Size.objects.get(code = remove_size)
                    except:
                        size = Size.objects.get(code = remove_size, gender=obj.gender)
                    obj.sizes.remove(size)
                obj.Birth_Place = data['Birth_Place']
                obj.Place_Residence = data['Place_Residence']
                obj.Address = data['Address']
                obj.Email = data['Email']
                obj.Phone = data['Phone']
                obj.save()
                response['id']= obj.id
                update_flag = True
            except:
                obj = Employee.objects.create(
                    code = data['code'],
                    firts_name = data['firts_name'],
                    second_name = data['second_name'],
                    short_name = data['short_name'],
                    gender = data['gender'],
                    document = data['document'],
                    number_doc = data['number_doc'],
                    Birth_Place = data['Birth_Place'],
                    Place_Residence = data['Place_Residence'],
                    Address = data['Address'],
                    Email = data['Email'],
                    Phone = data['Phone']
                )
                set_sizes = set({})
                set_data_sizes = set(data['sizes'])
                for size in obj.assignedsize_set.all():
                    set_sizes.add(size.size.code)
                data_difference = set_data_sizes.difference(set_sizes)
                actual_difference = set_sizes.difference(set_data_sizes)
                intersection_set = set_sizes.intersection(set_data_sizes)
                if data_difference:
                    for update_sizes in data_difference:
                        intersection_set.add(str(update_sizes))
                for size_code in intersection_set:
                    try: 
                        size = Size.objects.get(code = size_code)
                    except:
                        size = Size.objects.get(code = size_code, gender=obj.gender)
                    obj.sizes.add(size)
                for remove_size in actual_difference:
                    try: 
                        size = Size.objects.get(code = remove_size)
                    except:
                        size = Size.objects.get(code = remove_size, gender=obj.gender)
                    obj.sizes.remove(size)
                obj.save()
                response['id']= obj.id
                create_flag = True
        else:
            obj, is_create = Employee.objects.update_or_create( 
                code=data['code'],
                firts_name=data['firts_name'],
                second_name=data['second_name'],
                short_name=data['short_name'],
                gender=data['gender'],
                document=data['document'],
                number_doc=data['number_doc'],
                Birth_Place=data['Birth_Place'],
                Place_Residence=data['Place_Residence'],
                Address=data['Address'],
                Email=data['Email'],
                Phone=data['Phone']
                )
        response['codeResponse']= HTTP_200_OK
        response['messageResponse']= {True: _("OK. Created"), False: _("Ok. Update")}[is_create]
        response['id']= obj.id
    except:
        if create_flag == True and update_flag == None:
            response['codeResponse']= HTTP_200_OK
            response['messageResponse']= _("OK. Created")
        elif update_flag == True and create_flag == None:
            response['codeResponse']= HTTP_200_OK
            response['messageResponse']=  _("OK. Updated")
        else:                                   
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("Error. not created")
    return response

def syncronization_employee(ModelOrg, data, response):    
    response['code'] = data['code']
    response['short_name'] = data['short_name']    
    
    if ('cost_center' in data ):
        try:
            if data['cost_center'] is not None:
                data['cost_center'] =CostCenter.objects.get(code=data['cost_center'] )   
        except:
            print("Exception %s" % data['cost_center'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("cost_center. is null")            
    try:      
     
        data_create = format_data_employee(data)  
        print("update_or_create %s" % data_create)   
        obj, is_create = ModelOrg.objects.update_or_create( code=data['code'] ,  defaults = data_create)  
        print("in is_create %s" % is_create)      
        print("in obj %s" % obj)  
        response['codeResponse']= HTTP_200_OK
        response['messageResponse']= {True: _("OK. Created"), False: _("Ok. Update")}[is_create]
        response['id']= obj.id  
        for size in data['sizes']:
            try:
                print("size CREATE %s" % size)
                size_obj = Size.objects.get(code=size['code'],gender=size['gender'], body_area_id =size['body_area'] )
                print(size_obj)
                print(obj)
                size_create, is_size = AssignedSize.objects.update_or_create( employee=obj, size=size_obj ,  defaults = {'employee':obj,'size':size_obj})  
                print("in size_create %s" % size_create)   
                print("is_size obj %s" % is_size)  
            except:
                print("Exception size %s" % size )
                # response['codeResponse']= HTTP_400_BAD_REQUEST
                #response['messageResponse']= _("size. is null")     
    except:                                      
        response['codeResponse']= HTTP_400_BAD_REQUEST
        response['messageResponse']= _("Error. not created")
    return response    

def format_data_employee(data):
    return  {'code': data['code'], 
            'firts_name': data['firts_name'],
            'second_name': data['second_name'], 
            'last_name': data['last_name'], 
            'short_name': data['short_name'], 
            'gender': data['gender'], 
            'document': data['document'], 
            'number_doc': data['number_doc'], 
            'Birth_Place': data['Birth_Place'], 
            'Place_Residence':data['Place_Residence'], 'Address': data['Address'], 
            'Email': data['Email'], 
            'Phone': data['Phone']}

def check_response_errors(self_obj, data, response):
    if response['codeResponse'] != HTTP_200_OK: # en caso de tener errores
        serializer = self_obj.get_serializer(data=data, many=isinstance(data, list)) #se serializa
        serializer.is_valid() #se valida
        response['messageResponse'] = serializer.errors #se entrega un detalle del error
    return response       

