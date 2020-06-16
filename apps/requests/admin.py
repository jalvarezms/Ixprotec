from django.contrib import admin

from apps.requests.models import *


admin.site.register(RequestType)
admin.site.register(EmployeeRequest)
admin.site.register(DetailRequest)
admin.site.register(Status)
admin.site.register(WorkFlowApprovers)
