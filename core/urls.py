from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('elevation/ping', views.ping, name='ping'),
    path('elevation/lat/<str:lat>/lng/<str:lng>', views.elevation, name='elevation'),
]