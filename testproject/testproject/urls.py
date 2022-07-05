"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.shortcuts import render

import afterline.views as af_views


def template_view(tn):
    def v(r):
        return render(r, tn, {})

    return v


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name="registration/logout.html"), name='logout'),
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name='password_reset'),
    path('accounts/profile/', af_views.account_profile, name='profile'),
    path('accounts/register/', af_views.register_request, name='register'),
    path('', template_view("index.html"), name='index'),
    path('campaigns/create/', af_views.create_campaign, name='create_campaign'),
    path('campaign/<int:id>/', af_views.view_campaign, name='view_campaign'),
    path('campaigns/', af_views.my_campaigns, name='campaigns'),
]
