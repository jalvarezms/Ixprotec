
from apps.elements.models  import Classification, Element_Type 
from apps.equipments.models import Equipment, Supply
from apps.sizes.models import Area, Size
from apps.requests.models import RequestType, EmployeeRequest, Status, WorkFlowApprovers
from apps.inventories.models import CheckOutPut,CheckOutPutDetail
from apps.warehouses.models import Warehouse

def request_code(employee,request_type,request_cout ):
    return "%s-%s-%s" %(request_type.code,employee.code,request_cout)

def create_status(request,request_status, employee,observation ):
    status = request.status_set.all()  
    level_value = Status.CODE_CREATED  
    if status:
        print("existe")
        last_status = status.latest('id')
        print(last_status)
        level_value = last_status.level + 1
        status = Status.objects.create(
            level = level_value,
            observation = observation,
            status = request_status,
            employee_request = request,
            employee = employee
        )
        print(status)
        return status
    else:     
        print("No Existe")   
        status = Status.objects.create(
            level = level_value,
            observation = observation,
            status = request_status,
            employee_request = request,
            employee = employee
        )
        print(status)
        return status
    return 0     

def get_warehouse(employee):
    structure = employee.get_structure_last()
    if structure:
        company = structure.company
        departament = structure.departament
        division = structure.division
        warehouse = Warehouse.objects.filter(company = company,division = division, departament=departament )
        if warehouse:
            warehouse= warehouse.latest('id')
            return warehouse
    return ''


def create_orden_dispaht(request, status,warehouse):
    checout = CheckOutPut.objects.create(
      status = status,
      warehouse = warehouse,
      request =request
    ) 
    for detail in request.detailrequest_set.all():
        CheckOutPutDetail.objects.create(
            check_out   = checout,
            equipment   = detail.equipment,
            total_request= detail.total,
            request_detail     =detail
        ) 
    return checout
    

def get_approver_request(applicant, type_id,level):

    return WorkFlowApprovers.objects.get( applicant = applicant , request_type=type_id ,  level= level)
    


