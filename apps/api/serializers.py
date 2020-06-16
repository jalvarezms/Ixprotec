from rest_framework import serializers
from apps.organizational.models import Company, Division, Location, Position, structure, CostCenter, Position, BusinessUnit, Departament,structure
from apps.employees.models import (
    Employee
)
from apps.sizes.models import (
    Size,
    Area
)

from django.utils.translation import ugettext_lazy as _
from apps.employees.models import Employee, AssignedSize
from apps.sizes.models import Size,Area

from rest_framework.serializers import ModelSerializer
class CompanyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('code','name','status', 'start_date','country_code','country_name','city_name','telephone','address',)

class CompanyResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    codeResponse = serializers.CharField()
    messageResponse = serializers.CharField()
    class Meta:
        model = Company
        fields = ('id','code','name','codeResponse','messageResponse')        

class DivisionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ('code','name','status', 'start_date',)   

class DivisionResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    codeResponse = serializers.CharField()
    messageResponse = serializers.CharField()
    class Meta:
        model = Division
        fields = ('id','code','name','codeResponse','messageResponse')             

class LocationResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    codeResponse = serializers.CharField()
    messageResponse = serializers.CharField()
    class Meta:
        model = Location
        fields = ('id','code','name','codeResponse','messageResponse')  

class LocationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('code','name','status', 'start_date','group',)         
        
class BusinessUnitRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = ('code','name','status', 'start_date',)       

class BusinessUnitResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    codeResponse = serializers.CharField()
    messageResponse = serializers.CharField()
    class Meta:
        model = BusinessUnit
        fields = ('id','code','name','codeResponse','messageResponse')                

class DepartamentRequestSerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(slug_field='code', queryset=Departament.objects.all(), )
    class Meta:
        model = Departament
        fields = ('code','name','status','parent','head_boss', 'start_date',) 

class DepartamentReponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    codeResponse = serializers.CharField()
    messageResponse = serializers.CharField()
    class Meta:
        model = Departament
        fields = ('id','code','name','codeResponse','messageResponse')         

class CostCenterRequestSerializer(serializers.ModelSerializer):               
    company= serializers.SlugRelatedField(slug_field='code', queryset=Company.objects.all(), )
    class Meta:
        model = CostCenter
        fields = ('company','code','name','status', 'start_date',) 
        extra_kwargs = {    
                'company': {'required': True},
                'code': {'required': True},
                'name': {'required': True},
                'start_date': {'required': True},
                 }                       
class CostCenterResponseSerializer(serializers.ModelSerializer):               
    id = serializers.CharField()
    #company= serializers.SlugRelatedField(slug_field='code', queryset=Company.objects.all(), )
    codeResponse = serializers.CharField()
    messageResponse = serializers.CharField()
    class Meta:
        model = CostCenter
        fields = ('id','code','name','codeResponse','messageResponse')                        
class CostCenterSerializer(serializers.ModelSerializer):
    def validate(self, data):
        print("validate CostCenterSerializer")        
        
    company= serializers.SlugRelatedField(slug_field='code', queryset=Company.objects.all(), )
    class Meta:
        model = CostCenter
        fields = ('company','code','name','status', 'start_date',) 
        extra_kwargs = {    
                'company': {'required': False},
                'code': {'validators': []},
                'name': {'required': False},
                'start_date': {'required': False},
                 }
        validators = []           

class PositionRequestSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='code', queryset=Company.objects.all(), )
    parent = serializers.SlugRelatedField(slug_field='code', queryset=Position.objects.all(), )
    business_unit= serializers.SlugRelatedField(slug_field='code', queryset=BusinessUnit.objects.all(), )
    departament = serializers.SlugRelatedField(slug_field='code', queryset=Departament.objects.all(), )
    division = serializers.SlugRelatedField(slug_field='code', queryset=Division.objects.all(), )
    location = serializers.SlugRelatedField(slug_field='code', queryset=Location.objects.all(), )
    cost_center = serializers.SlugRelatedField(slug_field='code', queryset=CostCenter.objects.all(), )
    #business_unit = BusinessUnitSerializer()
    #departament = DepartamentSerializer()
    class Meta:
        model = Position        
        fields =  ('code','company','name','parent','business_unit','departament','cost_center','division','location','status', 'start_date') 

class PositionResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    #company= serializers.SlugRelatedField(slug_field='code', queryset=Company.objects.all(), )
    codeResponse = serializers.CharField()
    messageResponse = serializers.CharField()
    class Meta:
        model = CostCenter
        fields = ('id','code','name','codeResponse','messageResponse')  

class OrganizationalSerializer(serializers.ModelSerializer):

    company = CompanyRequestSerializer( )
    #business_unit = BusinessUnitSerializer()
    #departament = DepartamentSerializer()
    class Meta:
        model = Position
        
        fields = '__all__'             

class StructureRequestSerializer(ModelSerializer):
    employee = serializers.SlugRelatedField(slug_field='code', queryset=Employee.objects.all(), )
    company = serializers.SlugRelatedField(slug_field='code', queryset=Company.objects.all(), )
    division = serializers.SlugRelatedField(slug_field='code', queryset=Division.objects.all(), )
    location = serializers.SlugRelatedField(slug_field='code', queryset=Location.objects.all(), )
    businessUnit = serializers.SlugRelatedField(slug_field='code', queryset=BusinessUnit.objects.all(), ) 
    departament = serializers.SlugRelatedField(slug_field='code', queryset=Departament.objects.all(), )
    position = serializers.SlugRelatedField(slug_field='code', queryset=Position.objects.all(), )

    class Meta:
        model = structure
        fields = ('employee','company','division','location','businessUnit','departament','position','start_date', 'end_date') 

class StructureResponsetSerializer(ModelSerializer):
    id = serializers.CharField()
    employee =  serializers.CharField()
    company =  serializers.CharField()
    position =  serializers.CharField()
    start_date =  serializers.CharField()
    codeResponse = serializers.CharField()
    messageResponse = serializers.CharField()
    class Meta:
        model = structure
        fields = ('id','company','employee','position','start_date','codeResponse','messageResponse')          

   
        fields = '__all__' 

class AssignedSizeSerializer(serializers.ModelSerializer):
    employee= serializers.SlugRelatedField(slug_field='code', queryset=Employee.objects.all(), )
    size = serializers.SlugRelatedField(slug_field='code', queryset=Size.objects.all(), )
    class Meta:
        model = AssignedSize
        fields = ('employee', 'size',)

class BodyAreaSerializer(serializers.ModelSerializer):
    code = serializers.SlugRelatedField(slug_field='code', queryset=Area.objects.all(), )
    class Meta:
        model = Area
        #fields = ('id','code', 'name')
        fields = '__all__' 
class SizeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Size
        fields = ('id','code', 'gender','name','body_area')

class EmployeeRequestSerializer(serializers.ModelSerializer):
    #sizes = serializers.SlugRelatedField(slug_field='code', queryset=Size.objects.all(), many=True,)
    sizes = SizeSerializer(read_only=True, many=True)
    class Meta:
        model = Employee
        fields = ['code','firts_name','second_name','last_name','short_name','gender', 'document','number_doc','sizes','Birth_Place','Place_Residence','Address','Email','Phone',]

class EmployeeReponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    codeResponse = serializers.CharField()
    messageResponse = serializers.CharField()
    class Meta:
        model = Employee
        fields = ('id','code','short_name','codeResponse','messageResponse')  




class SizeListSerializer(ModelSerializer):
    # body_area = BodyAreaSerializer()
    body_area = serializers.SlugRelatedField(slug_field='code', queryset=Area.objects.all(), )
    gender = serializers.SerializerMethodField()
    class Meta:
        model = Size
        fields = ['code','gender','body_area','description','status','name']
    
    def get_gender(self, value):
        gender_text = value.gender_text() 
        return gender_text 
    

class SizeRequestSerializer(serializers.Serializer):
    code =  serializers.CharField(required=True)
    gender = serializers.IntegerField(required=True,min_value=0,max_value=2)
    body_area= serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    status = serializers.BooleanField(required=True)
    name = serializers.CharField(required=True)
 
    def validate_body_area(self,value):
        try:
            Area.objects.get(code=value)
        except:
            raise serializers.ValidationError(_("this body area CODE doesn't exist"))
        return value

    def create(self, validated_data):
        body_area_code=validated_data['body_area']
        obj_area = Area.objects.get(code=body_area_code)
        obj = Size.objects.create(
            code = validated_data['code'],              
            gender=validated_data['gender'],
            body_area=obj_area,
            description=validated_data['description'],
            status=validated_data['status'],
            name=validated_data['name']
        )
        return obj                         
    def update(self, validated_data):
        body_area_code=validated_data['body_area']
        obj_area = Area.objects.get(code=body_area_code)
        obj = Size.objects.get(code = validated_data['code'], gender= validated_data['gender'],body_area= obj_area)
        obj.description= validated_data['description']
        obj.status=validated_data['status']
        obj.name=validated_data['name']
        obj.save()
        return obj
class BodyAreaListSerializer(ModelSerializer):
    lookup_field = 'code'
    class Meta:
        model= Area
        fields = ('code','name','description','status')


class BodyAreaRequestSerializer(serializers.Serializer):
    code =  serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    status = serializers.BooleanField(required=True)

    def create(self, validated_data):
        obj = Area.objects.create(
            code = validated_data['code'],
            name=validated_data['name'],
            description=validated_data['description'],
            status=validated_data['status']
        )
        return obj

    def update(self, validated_data):
        obj = Area.objects.get(code = validated_data['code'])
        obj.name= validated_data['name']
        obj.description=validated_data['description']
        obj.status=validated_data['status']
        obj.save()
        return obj 
class ResponseSerializer(serializers.Serializer):
    messageResponse =  serializers.CharField()
    codeResponse =  serializers.CharField()
    # data = SizeRequestSerializer()
    data = serializers.CharField()
