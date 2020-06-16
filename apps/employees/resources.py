import tablib
from import_export import resources
from apps.employees.models import Employee
from import_export.signals import post_import
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .utils import create_user

class EmployeeResource(resources.ModelResource):

    class Meta:
        model = Employee
        skip_unchanged = True
        report_skipped = True
        import_id_fields  = ('code',)
        fields = ('code', 'firts_name', 'second_name', 'last_name', 'short_name', 'gender', 'document', 'number_doc', 'Birth_Place', 'Place_Residence', 'Address', 'Email', 'Phone',)

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        for row_index , row_values in enumerate(dataset):
            create_user(id = row_values[0])

class UserResource(resources.ModelResource):

    class Meta:
        model = User
        skip_unchanged = True
        report_skipped = True
        import_id_fields  = ('username',)
        fields = ('username', 'password', 'email', )
    
    def before_import(self, dataset, using_transactions, dry_run, **kwargs): 
        for row_index, row_values in enumerate(dataset):
            row = dict(zip(dataset.headers, row_values))
            if row['password']:
                row['password'] = make_password(row['password'])
                del dataset[row_index]
                dataset.insert(row_index, row.values())

