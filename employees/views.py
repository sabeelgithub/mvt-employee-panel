# views.py
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.db.models import Q

from .models import Employee
from .forms import EmployeeForm


class EmployeesList(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def get(self, request):
        employees = Employee.objects.filter(user=request.user).order_by('-created_at')
        search_term = request.GET.get('search', '')

        if search_term:
            employees = employees.filter(
                Q(name__icontains=search_term) |
                Q(position__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(custom_fields__icontains={search_term:""}) | # This checks for any key with the search term
                Q(custom_fields__icontains=search_term)  # This checks for values that match the search term
            )
       

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('employee_table_rows.html', {'employees': employees})
            return JsonResponse({'html': html})
        
        context = {
            'employees': employees,
            'search_term': search_term,
        }
        return render(request, 'employee_list.html', context)


class EmployeeCreate(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def get(self, request):
        form = EmployeeForm()
        return render(request, 'employee_form.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        print(request.POST,'data')
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': reverse('employee_list')})
            return redirect('employee_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                first_error_message = next(iter(form.errors.values()))[0]
                return JsonResponse({'success': False, 'error':first_error_message})
            return render(request, 'employee_form.html', {'form': form})


class EmployeeUpdate(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def get(self, request, id):
        employee = Employee.objects.filter(user=request.user).get(id=id)
        context = {
            'employee': employee,
            'is_update': True
        }
        return render(request, 'employee_form.html', context)
    
    @method_decorator(login_required)
    def post(self, request, id):
        print(request.POST,'data')
        employee = Employee.objects.filter(user=request.user).get(id=id)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': reverse('employee_view', args=[employee.id])})
            return redirect(reverse('employee_view', args=[employee.id]))
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                first_error_message = next(iter(form.errors.values()))[0]
                return JsonResponse({'success': False, 'error': first_error_message})
            return render(request, 'employee_form.html', {'form': form, 'is_update': True, 'employee': employee})


    
class SingleEmployeeDetail(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def get(self,request,id):
        employee = Employee.objects.filter(user=request.user).get(id=id)
        context = {
            'employee': employee
        }
        return render(request, 'employee_view.html', context)
    

class EmployeeDelete(View):
    @method_decorator(login_required)
    def delete(self, request, id):
        try:
            employee = Employee.objects.filter(user=request.user).get(id=id)
            employee.delete()
            return JsonResponse({'success': True}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Employee not found'}, status=404)