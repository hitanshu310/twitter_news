from django.urls import path
from . import views


urlpatterns = [
    path('', views.autho, name='index'),
    path('hello/', views.hello, name='index'),
    path('authenticate/', views.authorize, name='auth')
]
