from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # I'm using login_view to avoid naming conflicts with Django's built-in login function.
    path('verify/', views.verify, name='verify'),
]

