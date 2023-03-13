"""simple_django URL Configuration

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
from django.urls import path, include
from simple_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userratings/', userrating_list, name='userrating_list'),
    path('',home_view,name="home_view"),
    #path('',include('frontend.urls')),
    #path('',create_view,name='create'),
    # path('list/',list_view,name='list' ),
    #path('display_rating/',display_rating,name='display_rating'),
    path('enter/',add_MyUser,name='enter'),
    path('update/',update_MyUser,name='update'),

    path('logout/',logoutPage,name='logout'),
    path('edit_user/',edit_user,name='edit_user')

    # path('<id>/update',update_view,name='update'),
    # path('<id>/delete',delete_view,name='delete'),
]
