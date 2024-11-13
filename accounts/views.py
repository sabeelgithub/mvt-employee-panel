from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.views import View
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.conf.urls import handler404

from .forms import LoginForm,RegisterForm,ChangePasswordForm

class Home(View):
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('employee_list')
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }
                return JsonResponse({'success': True, 'redirect_url': reverse('employee_list')})

            return JsonResponse({'success': False, 'message':'Invalid username or password.'})
        
        errors = form.errors.get_json_data()
        return JsonResponse({'success': False, 'message': errors}, status=400)

class RegisterView(View):
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('employee_list')
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': reverse('home')})
                # return JsonResponse({'success': True, 'message': 'Your password was successfully updated!'})
            return redirect('employee_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = {field: [{'message': error} for error in error_list] for field, error_list in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors})
            return render(request, 'change_password.html', {'form': form})



class ChangePasswordView(LoginRequiredMixin, View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'change_password.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': reverse('employee_list'), 'message': 'Your password was successfully updated!'})
            return redirect('employee_list')
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': errors}, status=400)
            return render(request, 'change_password.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# Custom 404 error handler function
def custom_404(request, exception):
    return render(request, '404.html', status=404)

# Setting the custom handler
handler404 = custom_404

        
class Check(View):
    def get(self,request):
        try:
            return JsonResponse({"message":"checking","status":200})
        except Exception as e:
            return JsonResponse({"message":"error","status":500})