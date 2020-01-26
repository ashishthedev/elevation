from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('elevation/ping', views.ping, name='ping'),
    path('elevation/lat/<float:lat>/lng/<float:lng>', views.ping, name='elevation'),
]