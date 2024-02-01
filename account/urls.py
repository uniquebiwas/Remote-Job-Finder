from django.urls import path
from account import views
from django.contrib.auth import views as auth_views
# from .views import change_password
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
from .views import activate_user

app_name = "account"

urlpatterns = [

    path('employee/register/', views.employee_registration, name='employee-registration'),
    path('employer/register/', views.employer_registration, name='employer-registration'),
    path('profile/edit/<int:id>/', views.employee_edit_profile, name='edit-profile'),
    path('login/', views.user_logIn, name='login'),
    path('logout/', views.user_logOut, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate_user, name='activate'),

]
