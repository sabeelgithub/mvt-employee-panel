# views.py
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from .models import Employee
from .forms import EmployeeForm

class EmployeesList(View):

    @method_decorator(login_required)
    def get(self,request):
        employees = Employee.objects.filter(user=request.user).order_by('-created_at')
        print(request.user,'user')
        print(employees,'employees')
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
    
    def post(self,request):
        print(request.POST,'data')
        form = EmployeeForm(request.POST)
        if form.is_valid():
            print("un")

            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            messages.success(request, "Employee created successfully.")
            print('inke')
            return redirect('employee_list')
        else:
            messages.error(request, "There was an error creating the employee.")
            # Return the form with error messages if invalid
            return render(request, 'employee_form.html', {'form': form})





# @login_required
# def employee_create(request):
#     print(request.POST, 'POST data') 
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST)
#         # print(form,'form')
#         if form.is_valid():
#             employee = form.save(commit=False)
#             employee.user = request.user
#             employee.save()
#             messages.success(request, "Employee created successfully.")
#             print('inke')
#             return redirect('employee_list')
#         else:
#             messages.error(request, "There was an error creating the employee.")
#     else:
#         form = EmployeeForm()
    
#     return render(request, 'employee_form.html', {'form': form})

# @login_required
# def employee_create(request):
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST)
        
#         if form.is_valid():
#             employee = form.save(commit=False)
#             employee.user = request.user
#             employee.save()
            
#             if request.is_ajax():  # Check if it's an AJAX request
#                 return JsonResponse({'message': 'Employee created successfully.'})
#             else:
#                 messages.success(request, "Employee created successfully.")
#                 return redirect('employee_list')
#         else:
#             if request.is_ajax():
#                 return JsonResponse({'error': 'There was an error creating the employee.'}, status=400)
#             else:
#                 messages.error(request, "There was an error creating the employee.")
    
#     else:
#         form = EmployeeForm()

#     return render(request, 'employee_form.html', {'form': form})

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm

@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        
        if form.is_valid():
            employee = form.save(commit=False)
            print(employee,'dsf')
            employee.user = request.user
            print(employee.user,'user')
            employee.save()
            
            # Check if the request is an AJAX request using the header
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Employee created successfully.'})
            else:
                messages.success(request, "Employee created successfully.")
                return redirect('employee_list')
        else:
            # Handle error for form validation failure
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'There was an error creating the employee.'}, status=400)
            else:
                messages.error(request, "There was an error creating the employee.")
    
    else:
        form = EmployeeForm()

    return render(request, 'employee_form.html', {'form': form})


# class EmployeeCreate(View):
    
#     def get(self, request):
#         form = EmployeeForm()
#         return render(request, 'employee_form.html', {'form': form})

#     def post(self, request):
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             print(user,'user')
            
#             if user is not None:
#                 login(request, user)
#                 # Generate tokens if needed
#                 refresh = RefreshToken.for_user(user)
#                 tokens = {
#                     'access_token': str(refresh.access_token),
#                     'refresh_token': str(refresh),
#                 }
#                 # Redirect to a success page or return tokens if used in a JSON response.
#                 # return render(request, 'employee_list.html', {'tokens': tokens, 'user': user})
#                 return redirect('employee_list')
#                 # return render(request, 'dashboard.html', {'tokens': tokens, 'user': user})

#             form.add_error(None, 'Invalid username or password.')
        
#         # Re-render the form with an error message if invalid login attempt
#         return render(request, 'login.html', {'form': form})

@login_required
def employee_update(request, id):
    employee = get_object_or_404(Employee, id=id, user=request.user)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect('employee_list')
        else:
            messages.error(request, "There was an error updating the employee.")
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'employee_form.html', {'form': form, 'is_update': True})

