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
    # other paths...
    path('post_job/', views.post_job_opening, name='post_job'),
    path('job_data/', views.institute_job_data, name='institute_job_data'),
    path('edit_institute_profile/', views.edit_institute_profile, name='edit_institute_profile'),
    path('view_institute_profile/', views.view_institute_profile, name='view_institute_profile'),

    ##### Recruiter
   
    path('recruiter_dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('send_request/<int:institute_id>/', views.send_request, name='send_request'),
    path('requests/', views.institute_requests, name='institute_requests'),
    path('manage_request/<int:request_id>/', views.manage_request, name='manage_request'),
    
    
    path('institute_list', views.institute_list, name='institute_list'),
    path('list_shared_students/', views.list_shared_students, name='list_shared_students'),
    path('view_shared_students/<int:institute_id>/', views.view_shared_students, name='view_shared_students'),
    path('recruiter_student_profile/<str:username>/', views.recruiter_student_profile, name='recruiter_student_profile'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
