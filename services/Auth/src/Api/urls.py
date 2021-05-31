"""Conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import Api.views as vw_auth
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


urlpatterns = [
    path('', vw_auth.AuthUserView.as_view(), name="auth"),
    path('/token', obtain_jwt_token, name="login"),
    path('/token/verify', verify_jwt_token, name="token_verify"),
    path('/token/refresh', refresh_jwt_token, name="token_refresh")
]
