from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.views import View
from django.contrib import messages

from .forms import LoginForm,RegisterForm

class LoginView(View):
    
    def get(self, request):
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
                # return render(request, 'dashboard.html', {'tokens': tokens, 'user': user})

            form.add_error(None, 'Invalid username or password.')

        return render(request, 'login.html', {'form': form})


class RegisterView(View):
    
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to the login page or any other page
        
        return render(request, 'register.html', {'form': form})



# class ChangePassword(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     # function for changing password
#     @swagger_auto_schema(
#     operation_description="Change Password",
#     operation_id='change password',
#     request_body=ChangePasswordSerializer
#     ) 
#     def post(self,request):
#         try:
#             current_password = str(request.data.get("current_password"))
#             new_password = str(request.data.get("new_password"))
            
#             if len(new_password) < 5:
#                 return Response(password_length_issue(),status=status.HTTP_400_BAD_REQUEST)
            
#             if not check_password(current_password,request.user.password):
#                 return Response(user_password_does_not_match(),status=status.HTTP_400_BAD_REQUEST)
            
#             if check_password(new_password,request.user.password):
#                 return Response(user_password_same_as_previous(),status=status.HTTP_400_BAD_REQUEST)
            
#             user = CustomUser.objects.get(id=request.user.id)
#             user.set_password(str(new_password))
#             user.save()
#             return Response(user_password_change_success(),status=status.HTTP_200_OK)
        
#         except Exception as e:
#             return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class UserProfileData(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     # function for  user profile data 
#     @swagger_auto_schema(
#     operation_description="User Profile",
#     operation_id='user profile'
#     )       
#     def get(self,request):
#         try:
#             user = CustomUser.objects.get(id=request.user.id)
#             serializer = UserReadSerializer(user)
#             return Response(user_detail_success(serializer.data),status=status.HTTP_200_OK)
        
#         except Exception as e:
#             return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class Check(APIView):
#     def get(self,request):
#         try:
#             return Response({"message":"checking","status":status.HTTP_200_OK},status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)