from django.urls import path

from . import views

urlpatterns = [
    path('countryList/', views.country_list, name='country_list'),
]
