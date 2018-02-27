from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('message/', views.message, name='message'),
    path('web_hook/', views.web_hook, name='web_hook'),
]
