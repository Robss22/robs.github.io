from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import download_excel_template_view
from django.contrib import admin




app_name = 'student_app'

urlpatterns = [
    path('', views.home, name='home'), #Main Page, the applications starts from here
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact, name='contact'),
    path('applicationform/', views.applicationform, name='applicationform'),
    path('download/', views.download_view, name='download'),  # List of files to download
    path('download/<int:file_id>/', views.download_file, name='download_file'),  # Specific file download
    path('teacherdashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),  # Teacher dashboard
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),  # Admin dashboard
    path('upload_content/', views.upload_content_view, name='upload_content'),  # Upload content
    path('upload_marks/', views.upload_marks_view, name='upload_marks'),  # Upload marks
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout
    path('add_user/', views.add_user_view, name='add_user'),  # Add new user
    path('add_student/', views.add_student_view, name='add_student'),  # Add new student
    path('upload_bulk_students/', views.upload_bulk_students_view, name='upload_bulk_students'),  # Bulk upload students
    path('add_class/', views.add_class_view, name='add_class'),  # Add new class
    path('add_subject/', views.add_subject_view, name='add_subject'),  # Add new subject
    path('download_student_template/', views.download_student_template, name='download_student_template'),  # Download student template
    path('student_dashboard/', views.student_dashboard_view, name='student_dashboard'),  # Student dashboard
    path('download_excel_template/', download_excel_template_view, name='download_excel_template'),  # Download Excel template
]
