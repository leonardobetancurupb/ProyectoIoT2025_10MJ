from django.db import models
from django.contrib.auth.models import User

class SensorType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.type.name})"
    
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
