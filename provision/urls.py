from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('elevation/ping', views.ping, name='ping'),
    path('api/startProvisioning/<str:zoneName>', views.startProvisioning, name='startProvisioning'),
    path('api/provisioningCurrentState/<str:zoneName>', views.provisioningCurrentState, name='provisioningCurrentState'),
]