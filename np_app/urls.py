'''
Description: This file defines the URL patterns for the np_app application.
Author(s): Michael Sousa Jr.
Last Modified Date: 27 October 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/ref/urls/
'''
from django.urls import path
from .views import index, breaches_page, about_page, notify_page, success_view

urlpatterns = [
    path('', index, name='index'),
    path('breaches/', breaches_page, name='breaches'),
    path('about/', about_page, name='about'),
    path('notify/', notify_page, name='signup'),
    path('success/', success_view, name='success'),
]
