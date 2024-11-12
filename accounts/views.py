from django.shortcuts import render, redirect
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

class LoginView(View):
    
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('employee_list')
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

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
                return redirect('employee_list')

            form.add_error(None, 'Invalid username or password.')

        return render(request, 'login.html', {'form': form})


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
            return redirect('login')
        
        return render(request, 'register.html', {'form': form})
    
        
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
            # messages.success(request, 'Your password was successfully updated!')
            return redirect('employee_list')  
        return render(request, 'change_password.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


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