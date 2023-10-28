'''
Description: This file defines the URL patterns for the np_app application.
Author(s): Michael Sousa Jr.
Last Modified Date: 27 October 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/ref/urls/
'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('breaches/', views.breaches_page, name='breaches'),
    path('about/', views.about_page, name='about'),
    path('notify/', views.notify_page, name='notify'),
]
