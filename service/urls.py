from django.urls import path
from . import views

urlpatterns = [
    path('countryList/', views.country_list, name='countryList'),
    path('studyList/', views.study_list, name='countryList'),
]
