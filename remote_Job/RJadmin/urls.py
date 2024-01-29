from django.urls import path
from RJadmin import views
from django.contrib.auth import views as auth_views
app_name = "RJadmin"


urlpatterns = [
    path('courselogin/', views.login_view, name='login'),
    path('course/admin/', views.admin_page, name='admin_page'),
    path('edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('course/change_password/', views.change_password, name='change_password'),
    path('enroll/', views.enroll_course, name='enroll_course'),
    path('courselogout/', views.logout_view, name='logout'),


]
