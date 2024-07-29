"""
URL configuration for drfAuth2 project.

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
from django.urls import path,include
from base import views
from frontend import views as fe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/student/login/', views.StudentLoginView.as_view(), name='student-login'),
    path('api/student/register/', views.StudentRegistrationView.as_view(), name='student-register'),
    path('api/student/profile/', views.StudentProfileCreateView.as_view(), name='student-profile-create'),
    path('profiles/<int:pk>/', views.StudentProfileCreateView.as_view(), name='profile-detail-update'),

    #frontend

    path("login",fe.LoginPage),
    path("p",fe.profilePage),
    path("d",fe.Dashboard,name="dashboard"),
    path("la",fe.login_again),
    path('api/check_session/', fe.check_session, name='check_session'),

    path('api-auth/', include('rest_framework.urls'))
]
