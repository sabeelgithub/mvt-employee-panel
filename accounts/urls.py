from django.urls import path
from .views import *
from .views import logout_view

urlpatterns = [

    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', ChangePasswordView.as_view(),name='change_password'),
    path('check/',Check.as_view()),

]
    