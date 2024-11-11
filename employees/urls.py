from django.urls import path
from .views import *

urlpatterns = [
    path('list/', EmployeesList.as_view(), name='employee_list'),
    path('create/', EmployeeCreate.as_view(), name='employee_create'),
    path('view/<uuid:id>/', SingleEmployeeDetail.as_view(), name='employee_view'),
    path('update/<uuid:id>/', EmployeeUpdate.as_view(), name='employee_update'),
    path('delete/<uuid:id>/', EmployeeDelete.as_view(), name='employee_delete')
]

    
    