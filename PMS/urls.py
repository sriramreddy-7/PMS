"""
URL configuration for PMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("test/", views.test, name="test"),
    
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("recruiter_dashboard/", views.recruiter_dashboard, name="recruiter_dashboard"),
    path("institute_dashboard/", views.institute_dashboard, name="institute_dashboard"),
    path('bulk_student_upload/', views.bulk_student_upload, name='bulk_student_upload'),
    path('student_details/',views.student_details,name="student_details"),
    path('student/<str:username>/', views.student_profile, name='student_profile'),
    path('student_account/<str:username>/',views.student_account,name='student_account'),
    path('student_details_update',views.student_details_update,name='student_details_update'),
    path('student_job_openings/', views.student_job_openings, name='student_job_openings'),
    
    path("institute_job_applications//<int:job_id>/",views.institute_job_applications,name="institute_job_applications"),
    path('student_job_applications/', views.student_job_applications, name='student_job_applications'),
    path("institute_student_off_campus_jobs_status",views.institute_student_off_campus_jobs_status,name="institute_student_off_campus_jobs_status"),
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    
    # other paths...
    path('all_recruiters/', views.all_recruiters, name='all_recruiters'),
    
    
    path('post_job/', views.post_job_opening, name='post_job'),
    path('job_data/', views.institute_job_data, name='institute_job_data'),
    path('edit_institute_profile/', views.edit_institute_profile, name='edit_institute_profile'),
    path('view_institute_profile/', views.view_institute_profile, name='view_institute_profile'),

    ##### Recruiter
   
    path('recruiter_dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('send_request/<int:institute_id>/', views.send_request, name='send_request'),
    path('requests/', views.institute_requests, name='institute_requests'),
    path('manage_request/<int:request_id>/', views.manage_request, name='manage_request'),
    path('recruiter_profile/', views.recruiter_profile, name='recruiter_profile'),
    path('edit_recruiter_profile/', views.edit_recruiter_profile, name='edit_recruiter_profile'),

    path('institute_list', views.institute_list, name='institute_list'),
    path('list_shared_students/', views.list_shared_students, name='list_shared_students'),
    path('view_shared_students/<int:institute_id>/', views.view_shared_students, name='view_shared_students'),
    path('recruiter_student_profile/<str:username>/', views.recruiter_student_profile, name='recruiter_student_profile'),
    path('institute_profile/<int:institute_id>/', views.institute_profile, name='institute_profile'),
    path('institute_job_applications_detail/<int:job_id>/', views.institute_job_applications_detail, name='institute_job_applications_detail'),
    path('send_welcome_email', views.send_welcome_email, name='send_welcome_email'),
    path('single_student_upload/', views.single_student_upload, name='single_student_upload'),
    path('toggle_visibility/<str:username>/', views.toggle_visibility, name='toggle_visibility'),
    
    
    
    path('institute_student_on_campus_jobs_status/', views.institute_student_on_campus_jobs_status, name='institute_student_on_campus_jobs_status'),
    path('job_applications_on_campus_list/<int:job_id>/', views.job_applications_on_campus_list, name='job_applications_on_campus_list'),
    
    
    
    
    ##### Requests:
    path('institute_received-requests/', views.institute_received_requests, name='institute_received_requests'),
    path('recruiter_received-requests/', views.recruiter_received_requests, name='recruiter_received_requests'),
    path('institute_manage_request/<int:request_id>/', views.manage_institute_request, name='manage_institute_request'),
    path('recruiter_manage_request/<int:request_id>/', views.manage_recruiter_request, name='manage_recruiter_request'),
    path('ats_search/', views.ats_search, name='ats_search'),
    
    path('student_portfolio/<str:username>/', views.student_portfolio, name='student_portfolio'),
    path('upload_document/', views.upload_document, name='upload_document'),
    ##password reset
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
