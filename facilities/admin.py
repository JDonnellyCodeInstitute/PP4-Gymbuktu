from django.contrib import admin

# Register your models here.
from .models import Facilitie

@admin.register(Facilitie)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'max_capacity')