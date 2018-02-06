from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('message/', views.message, name='message'),
    path('test/', views.test, name='test'),
    path('adapter/', views.adapter, name='adapter'),
]
