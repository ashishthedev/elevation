from django.contrib import admin
from provision.models import Provisioner

@admin.register(Provisioner)
class ProvisionersAdmin(admin.ModelAdmin):
    pass