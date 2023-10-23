from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('breaches/', views.breaches_page, name='breaches'),
    path('about/', views.about_page, name='about'),
    path('notify/', views.notify_page, name='notify'),
]
