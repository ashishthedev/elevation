from django.urls import path
from . import views

urlpatterns = [
    path('api/startProvisioning/<str:zoneName>', views.startProvisioning, name='startProvisioning'),
    path('api/provisioningCurrentState/<str:zoneName>', views.provisioningCurrentState, name='provisioningCurrentState'),
]