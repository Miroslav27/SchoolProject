"""School_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.http import request
from journal import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',LoginView.as_view(template_name="login.html"),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('', views.IndexView.as_view(), name="home"),
    path('courses_by_cat/<int:category_id>/', views.CourseByCategoryView.as_view(), name="courses_by_cat"),
    path('create_student/', views.StudentCreateView.as_view(), name="student_create"),
    path('student/<int:student_id>/edit/',views.StudentEditView.as_view(), name="student_edit"),
    path('students_by_course/<int:course_id>/', views.StudentByCourseView.as_view(), name="students_by_course"),
    path('create_fakes/', views.CreateFakesView.as_view(),name="create_fakes"),
    path('create_course/',views.CourseCreateView.as_view(), name="course_create"),
    path('course/<int:course_id>/edit/',views.CourseEditView.as_view(), name="course_edit"),
    path('__debug__/', include('debug_toolbar.urls')),
              ]
