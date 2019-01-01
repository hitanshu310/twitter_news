from django.urls import path
from . import views


urlpatterns = [
    path('', views.checkAuth, name='index'),
    path('hello/', views.hello, name='hello'),
    path('authenticate/', views.authorize, name='auth1'),
    path('authorize/', views.autho, name='auth2'),
    path('feed/',  views.feed, name='feed'),
    path('logout/', views.logout, name='logout'),
]
