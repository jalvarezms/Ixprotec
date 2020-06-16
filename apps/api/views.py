from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from rest_framework import views
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
import sys
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from apps.api.serializers import (
    CompanyRequestSerializer,
    CompanyResponseSerializer,
    DivisionRequestSerializer,
    DivisionResponseSerializer,
    LocationResponseSerializer,
    LocationRequestSerializer,
    CostCenterSerializer,
    OrganizationalSerializer, 
    BusinessUnitRequestSerializer, 
    BusinessUnitResponseSerializer, 
    DepartamentRequestSerializer, 
    DepartamentReponseSerializer, 
    CostCenterRequestSerializer, 
    CostCenterResponseSerializer, 
    PositionRequestSerializer,
    PositionResponseSerializer,
    StructureRequestSerializer,
    StructureResponsetSerializer,
    EmployeeRequestSerializer,
    EmployeeReponseSerializer,
    SizeListSerializer,
    ResponseSerializer,
    SizeRequestSerializer,
    BodyAreaListSerializer,
    BodyAreaRequestSerializer
)
from apps.organizational.models import Company, Division, Location, CostCenter, Position, BusinessUnit, Departament, structure
# Create your views here.
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import *
from apps.api.util.organizational_api import syncronization_upsert,syncronization_upsert_job_info,get_response_code_name,check_response_errors, get_response_jobinfo
from apps.employees.models import Employee
from rest_framework.generics import ListCreateAPIView
from apps.api.util.employee_api import employee_sync, employee_response, syncronization_employee
from apps.sizes.models import (
    Size, 
    Area
)


class CompanyList(generics.ListCreateAPIView):

    queryset = Company.objects.all()
    serializer_class = CompanyRequestSerializer

    def get_queryset(self):
        queryset = Company.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        results = []        
        for row_data in request.data:           
            response = syncronization_upsert(Company,row_data ,get_response_code_name())
            results.append(check_response_errors(self, row_data, response))
        output_serializer = CompanyResponseSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)   


class DivisionList(generics.ListCreateAPIView):

    queryset = Division.objects.all()
    serializer_class = DivisionRequestSerializer

    def get_queryset(self):
        queryset = Division.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        results = []        
        for row_data in request.data:      
            response = syncronization_upsert(Division,row_data ,get_response_code_name())           
            results.append(check_response_errors(self, row_data, response))    
        output_serializer = DivisionResponseSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)   

class LocationList(generics.ListCreateAPIView):

    queryset = Location.objects.all()
    serializer_class = LocationRequestSerializer

    def get_queryset(self):
        queryset = Location.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        results = []        
        for row_data in request.data:      
            response = syncronization_upsert(Location,row_data ,get_response_code_name())           
            results.append(check_response_errors(self, row_data, response))     
        output_serializer = LocationResponseSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)  

class BusinessUnitList(generics.ListCreateAPIView):

    queryset = BusinessUnit.objects.all()
    serializer_class = BusinessUnitRequestSerializer

    def get_queryset(self):
        queryset = BusinessUnit.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        results = []        
        for row_data in request.data:      
            response = syncronization_upsert(BusinessUnit,row_data ,get_response_code_name())           
            results.append(check_response_errors(self, row_data, response))   
        output_serializer = BusinessUnitResponseSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)          

class DepartamentList(generics.ListCreateAPIView):

    queryset = Departament.objects.all()
    serializer_class = DepartamentRequestSerializer

    def get_queryset(self):
        queryset = Departament.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        results = []        
        for row_data in request.data:      
            response = syncronization_upsert(Departament,row_data ,get_response_code_name())           
            results.append(check_response_errors(self, row_data, response))   
        output_serializer = DepartamentReponseSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)   

class CostCenterList(generics.ListCreateAPIView):

    queryset = CostCenter.objects.all()
    serializer_class = CostCenterRequestSerializer

    def get_queryset(self):
        queryset = CostCenter.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        results = []        
        for row_data in request.data:      
            response = syncronization_upsert(CostCenter,row_data ,get_response_code_name())           
            results.append(check_response_errors(self, row_data, response))    
        output_serializer = CostCenterResponseSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)  

class PositionList(generics.ListCreateAPIView):

    queryset = Position.objects.all()
    serializer_class = PositionRequestSerializer

    def get_queryset(self):
        queryset = Position.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        print(type(Position))
        results = []        
        for row_data in request.data:      
            response = syncronization_upsert(Position,row_data ,get_response_code_name())           
            results.append(check_response_errors(self, row_data, response))      
        output_serializer = PositionResponseSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

class EmployeeList(generics.ListCreateAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeRequestSerializer

    def get_queryset(self):
        queryset = Employee.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        results = []      
        for row_data in request.data: 
            #response = employee_sync(row_data, employee_response())  
            response = syncronization_employee(Employee,row_data, employee_response())
            results.append(response)       
        output_serializer = EmployeeReponseSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

class StructureList(ListCreateAPIView):
    queryset= structure.objects.all()
    serializer_class = StructureRequestSerializer

    def get_queryset(self):
        queryset = structure.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        results = []        
        for row_data in request.data:      
            response = syncronization_upsert_job_info(structure,row_data ,get_response_jobinfo())        #se asigna response jobinfo    
            results.append(check_response_errors(self, row_data, response))      
        
        #print("resultaldos %s" % results)
        output_serializer = StructureResponsetSerializer(results, many=True)
        #print("output_serializer %s" % output_serializer)
        data = output_serializer.data[:]
        return Response(data)

class SizeList(APIView):

    permission_classes = []

    def get(self,request):
        queryset = Size.objects.all()
        List=SizeListSerializer(queryset, many=True)
        return Response(List.data)

    def post(self,request, *args, **kwargs):
        results = []
        for sizeItem in request.data:
            jsonDat= SizeRequestSerializer(data = sizeItem)
            if(jsonDat.is_valid()):
                body_area_code=sizeItem['body_area']
                obj_area = Area.objects.get(code=body_area_code)
                is_create = Size.objects.filter(code = sizeItem['code'], gender= sizeItem['gender'],body_area= obj_area).exists()
                if is_create:
                    jsonDat.update(validated_data=jsonDat.data)
                else:
                    jsonDat.create(validated_data=jsonDat.data)    

                messageResponse = {False: _("OK. Created"), True: _("Ok. Update")}[is_create]               
                results.append({'messageResponse':str(messageResponse) ,'codeResponse':HTTP_200_OK,'data':sizeItem })
            else:
                results.append({'messageResponse':str(jsonDat.errors) ,'codeResponse':HTTP_400_BAD_REQUEST,'data':sizeItem })

        respons=ResponseSerializer(data=results,many=True)
        respons.is_valid() #you have to execute at least one this method in order to serializer make its work and don't give you an error!
        return Response(respons.data)


class AreaList(ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = BodyAreaListSerializer

    def get_queryset(self):
        queryset = Area.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        results = []   
        for bodyAreaItem in request.data:
            jsonDat= BodyAreaRequestSerializer(data = bodyAreaItem)
            if(jsonDat.is_valid()):
                is_create = Area.objects.filter(code = bodyAreaItem['code']).exists()
                if is_create:
                    jsonDat.update(validated_data=jsonDat.data)
                else:
                    jsonDat.create(validated_data=jsonDat.data) 

                messageResponse = {False: _("OK. Created"), True: _("Ok. Update"),}[is_create]               
                results.append({'messageResponse':str(messageResponse) ,'codeResponse':HTTP_200_OK,'data':bodyAreaItem })
            else:
                
                results.append({'messageResponse':str(jsonDat.errors) ,'codeResponse':HTTP_400_BAD_REQUEST,'data':bodyAreaItem })

        output_serializer = ResponseSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)