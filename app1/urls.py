"""
URL configuration for chart project.

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
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('predict', views.Predict.as_view(), name='predict'),
    path('intro', views.Intro.as_view(), name='intro'),
    re_path(r'^search', views.Search.as_view(), name='search'),
    re_path(r'^history$', views.History.as_view(), name='history'),
    path('history/<str:str_id>', views.Detail.as_view(), name='detail'),
    # url 表待改
]
