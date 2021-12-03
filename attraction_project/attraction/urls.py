from django.shortcuts import render
from django.urls import path
from . import views
# Create your views here.

urlpatterns = [
    path('', views.index),
    path('attraction1/', views.attraction_page1),
    path('attraction2/', views.attraction_page2)
]
