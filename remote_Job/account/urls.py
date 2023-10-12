from django.urls import path
from account import views
from django.contrib.auth import views as auth_views
# from .forms import PasswordResetForm
# from .forms import CustomPasswordResetForm



app_name = "account"

urlpatterns = [

    path('employee/register/', views.employee_registration, name='employee-registration'),
    path('employer/register/', views.employer_registration, name='employer-registration'),
    path('profile/edit/<int:id>/', views.employee_edit_profile, name='edit-profile'),
    path('login/', views.user_logIn, name='login'),
    path('logout/', views.user_logOut, name='logout'),
    #password reset
    # path('forgot-password/', views.forgot_password, name='forgot_password'),
    # path('reset-password/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    

]
