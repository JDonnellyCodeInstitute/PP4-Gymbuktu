from django.contrib import admin
from .models import Facilitie


@admin.register(Facilitie)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'max_capacity')
