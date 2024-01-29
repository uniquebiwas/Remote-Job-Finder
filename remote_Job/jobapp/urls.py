from django.urls import path
from jobapp import views

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404


app_name = "jobapp"


urlpatterns = [

    path('', views.home_view, name='home'),
    path('jobs/', views.job_list_View, name='job-list'),
    path('job/create/', views.create_job_View, name='create-job'),
    path('job/<int:id>/', views.single_job_view, name='single-job'),
    path('apply-job/<int:id>/', views.apply_job_view, name='apply-job'),
    path('bookmark-job/<int:id>/', views.job_bookmark_view, name='bookmark-job'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('terms-condition/', views.terms_condition_view, name='terms-condition'),
    path('courses/', views.courses_view, name='courses'),
    path('result/', views.search_result_view, name='search_result'),
    path('course/<int:id>/', views.single_course_view, name='single-course'),
    path('apply-course/<int:id>/', views.apply_course_view, name='apply-course'),
    path('meeting/',views.videocall, name='meeting'),
    path('join/',views.join_room, name='join_room'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/employer/job/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('dashboard/employer/job/edit/<int:id>', views.job_edit_view, name='edit-job'),
    path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('dashboard/employer/close/<int:id>/', views.make_complete_job_view, name='complete'),
    path('dashboard/employer/delete/<int:id>/', views.delete_job_view, name='delete'),
    path('dashboard/employee/delete-bookmark/<int:id>/', views.delete_bookmark_view, name='delete-bookmark'),
    path('send-email/', views.send_email, name='send_email'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)