from django.contrib import admin
from .models import SensorType, Sensor, SensorData

@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location', 'owner', 'is_active', 'created_at')
    list_filter = ('type', 'is_active')
    search_fields = ('name', 'location', 'owner__username')
    date_hierarchy = 'created_at'

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'timestamp', 'value', 'unit')
    list_filter = ('sensor', 'unit')
    search_fields = ('sensor__name',)
    date_hierarchy = 'timestamp'
