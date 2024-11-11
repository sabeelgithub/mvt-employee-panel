from django.urls import path
from .views import *

urlpatterns = [
    path('list/', EmployeesList.as_view(), name='employee_list'),
    path('create/', EmployeeCreate.as_view(), name='employee_create'),
    # path('update/<int:id>/', views.employee_update, name='employee_update'),
]

    
    