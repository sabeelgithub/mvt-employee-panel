from django.urls import path
from .views import *

urlpatterns = [

    path('', LoginView.as_view(), name='login'),
    # path('create/',RegisterView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    # path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    # path('change-password/', ChangePassword.as_view()),
    # path('profile/', UserProfileData.as_view()),
    # path('check/',Check.as_view()),

]
    