from apps.organizational.models import Company, Division, Location, CostCenter, Position, Departament, structure, BusinessUnit
from apps.employees.models import Employee
# Create your views here.
from django.utils.translation import ugettext_lazy as _
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.core.exceptions import (
    NON_FIELD_ERRORS, FieldError, ImproperlyConfigured, ValidationError,
)


def get_response_code_name():
    return { 'id':'', 'code':'', 'name':'','codeResponse':'','messageResponse':'Ok' } 

def get_response_jobinfo():
    return {'id':'','company':'','employee':'','position':'','codeResponse':'','messageResponse':'Ok'  }

def syncronization_upsert(ModelOrg, data, response):    
    response['code'] = data['code']
    response['name'] = data['name']    
    if 'company' in data:
        print("in company %s" % data)
        try:
            if data['company'] is not None:
                data['company'] =Company.objects.get(code=data['company'] )   
        except:
            print("Exception %s" % data['company'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("company. is null")
    if 'division' in data:
        print("in Division %s" % data)
        try:
            if data['division'] is not None:
                data['division'] =Division.objects.get(code=data['division'] )   
        except:
            print("Exception %s" % data['division'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("division. is null")
    if 'location' in data:
        print("in location %s" % data)
        try:
            if data['location'] is not None:
                data['location'] =Location.objects.get(code=data['location'] )   
        except:
            print("Exception %s" % data['location'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("location. is null")
    if 'departament' in data:
        print("in departament %s" % data) 
        try:
            if data['departament'] is not None:
                data['departament'] =Departament.objects.get(code=data['departament'] )   
        except:
            print("Exception %s" % data['departament'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("departament. is null")    
    if 'business_unit' in data:
        print("in business_unit %s" % data)
        try:
            if data['business_unit'] is not None:
                data['business_unit'] =BusinessUnit.objects.get(code=data['business_unit'] )   
        except:
            print("Exception %s" % data['business_unit'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("business_unit. is null")
    if ('parent' in data ):
        try:
            if data['parent'] is not None:
                data['parent'] =ModelOrg.objects.get(code=data['parent'] )   
        except:
            print("Exception %s" % data['parent'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("parent. is null")
    if ('cost_center' in data ):
        try:
            if data['cost_center'] is not None:
                data['cost_center'] =CostCenter.objects.get(code=data['cost_center'] )   
        except:
            print("Exception %s" % data['cost_center'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("cost_center. is null")            
    try:      
        print("update_or_create %s" % data)      
        obj, is_create = ModelOrg.objects.update_or_create( code=data['code'] ,  defaults = data)  
        print("in is_create %s" % is_create)      
        print("in obj %s" % obj)  
        response['codeResponse']= HTTP_200_OK
        response['messageResponse']= {True: _("OK. Created"), False: _("Ok. Update")}[is_create]
        response['id']= obj.id  
    except:                                      
        response['codeResponse']= HTTP_400_BAD_REQUEST
        response['messageResponse']= _("Error. not created")
    return response    


def check_response_errors(self_obj, data, response):
    if response['codeResponse'] != HTTP_200_OK: # en caso de tener errores
        serializer = self_obj.get_serializer(data=data, many=isinstance(data, list)) #se serializa
        serializer.is_valid() #se valida
        response['messageResponse'] = serializer.errors #se entrega un detalle del error
    return response       

def syncronization_upsert_job_info(ModelOrg, data, response):    
    response['employee'] = data['employee']
    response['company'] = data['company']    
    response['position'] = data['position']  
    response['start_date'] = data['start_date'] 
    if 'company' in data:
        response['company'] = data['company']
        #print("in company %s" % data)
        try:
            if data['company'] is not None:
                company = Company.objects.get(code=data['company'] ) 
                data['company'] = company
        except:
            #print("Exception %s" % data['company'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("company. is null")
    if 'division' in data:
        #print("in Division %s" % data)
        try:
            if data['division'] is not None:
                data['division'] =Division.objects.get(code=data['division'] )    
        except:
            #print("Exception %s" % data['division'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("division. is null")
    if 'location' in data:
        #print("in location %s" % data)
        try:
            if data['location'] is not None:
                data['location'] =Location.objects.get(code=data['location'] )   
        except:
            #print("Exception %s" % data['location'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("location. is null")
    if 'departament' in data:
        #print("in departament %s" % data) 
        try:
            if data['departament'] is not None:
                data['departament'] =Departament.objects.get(code=data['departament'] )
        except:
            #print("Exception %s" % data['departament'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("departament. is null")    
    if 'businessUnit' in data:
        #print("in businessUnit %s" % data)
        try:
            if data['businessUnit'] is not None:
                data['businessUnit'] =BusinessUnit.objects.get(code=data['businessUnit'] )   
        except:
            #print("Exception %s" % data['business_unit'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("business_unit. is null")

    if ('employee' in data ):
        response['employee'] = data['employee']
        try:
            if data['employee'] is not None:
                employee = Employee.objects.get(code=data['employee'] )  
                data['employee'] = employee
        except:
            #print("Exception %s" % data['employee'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("employee. is null")    
    if ('position' in data ):
        response['position'] = data['position']
        try:
            if data['position'] is not None:
                position = Position.objects.get(code=data['position'] ) 
                data['position'] = position
        except:
            #print("Exception %s" % data['position'] )
            response['codeResponse']= HTTP_400_BAD_REQUEST
            response['messageResponse']= _("position. is null")                                     
    try:      
        print("-------------update_or_create----------------------")             
        obj, is_create = ModelOrg.objects.update_or_create( company=data['company'],employee=data['employee'],start_date=data['start_date']   ,  defaults = data)  
        print("-------------is_create----------------------")
        print("in is_create %s" % is_create)      
        print("in obj %s" % obj)  
        response['codeResponse']= HTTP_200_OK
        response['messageResponse']= {True: _("OK. Created"), False: _("Ok. Update")}[is_create]
        response['id']= obj.id  
    except:   
        print("except-------------------------")                                   
        response['codeResponse']= HTTP_400_BAD_REQUEST
        response['messageResponse']= _("Error. not created")
    return response                 