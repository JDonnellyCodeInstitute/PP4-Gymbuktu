from django.contrib import admin

# Register your models here.
from .models import Facility

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'max_capacity')