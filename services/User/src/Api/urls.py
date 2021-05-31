"""UserService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import Api.views as vw_user
from django.urls import path, include
#
urlpatterns = [
    path('', vw_user.UserCreateView.as_view(), name='register'),
    path('/list/all', vw_user.UserListView.as_view(), name='list_all'),
    path('/list/<slug:identifier>', vw_user.UserDetailView.as_view(), name='detail'),
]
