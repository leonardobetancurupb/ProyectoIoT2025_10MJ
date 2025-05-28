from django.db import models
from django.contrib.auth.models import User
import uuid

class SensorType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Sensor(models.Model):
    sensor_id = models.CharField(max_length=100, unique=True, default="AUTO_GENERATED", help_text="Unique identifier for the sensor")
    name = models.CharField(max_length=100, blank=True)  # Auto-generated from sensor_id
    type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=100, default="measurement", help_text="Parameter measured by this sensor (e.g., temperature, humidity)")
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Auto-generate sensor_id if it's the default value
        if self.sensor_id == "AUTO_GENERATED":
            self.sensor_id = f"SENSOR_{str(uuid.uuid4())[:8].upper()}"
        
        # Auto-generate name if not provided
        if not self.name:
            self.name = f"{self.sensor_id} ({self.parameter})"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.sensor_id} - {self.parameter} ({self.type.name})"
    
    class Meta:
        ordering = ['name']

class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='data', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.sensor.name}: {self.value} {self.unit} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
