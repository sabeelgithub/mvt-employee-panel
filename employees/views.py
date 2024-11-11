# views.py
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse

from .models import Employee
from .forms import EmployeeForm

class EmployeesList(View):

    @method_decorator(login_required)
    def get(self,request):
        employees = Employee.objects.filter(user=request.user).order_by('-created_at')
        search_term = request.GET.get('search', '')

        if search_term:
            employees = employees.filter(name__icontains=search_term)

        context = {
            'employees': employees,
            'search_term': search_term,
        }
        return render(request, 'employee_list.html', context)


class EmployeeCreate(View):
    @method_decorator(login_required)
    def get(self,request):
        form = EmployeeForm()
        return render(request,'employee_form.html',{'form': form})
    
    @method_decorator(login_required)
    def post(self,request):
            form = EmployeeForm(request.POST)
            if form.is_valid():
                employee = form.save(commit=False)
                employee.user = request.user
                employee.save()
                messages.success(request, "Employee created successfully.")
                return redirect('employee_list')
            else:
                messages.error(request, "There was an error creating the employee.")
                return render(request, 'employee_form.html', {'form': form})
      
            
class SingleEmployeeDetail(View):
    @method_decorator(login_required)
    def get(self,request,id):
        employee = Employee.objects.filter(user=request.user).get(id=id)
        context = {
            'employee': employee
        }
        return render(request, 'employee_view.html', context)



class EmployeeUpdate(View):
    @method_decorator(login_required)
    def get(self,request,id):
        employee = Employee.objects.filter(user=request.user).get(id=id)
        context = {
            'employee': employee,
            'is_update':True
        }
        return render(request, 'employee_form.html', context)
    
    def post(self,request,id):
        employee = Employee.objects.filter(user=request.user).get(id=id)
        
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully.")

            return redirect(reverse('employee_view', args=[employee.id]))
        else:
            messages.error(request, "There was an error creating the employee.")
            context = {
            'employee': employee,
            'is_update':True
            }
            return render(request, 'employee_form.html', context)



