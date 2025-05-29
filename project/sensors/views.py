from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max, Min, Avg
import math
import random

from .models import Sensor, SensorData, SensorType
from .forms import SensorForm, SensorTypeForm, SensorFilterForm, ManualDataEntryForm
from .utils import prepare_time_series_data, generate_demo_data
from .external_service import ExternalSensorService

class DashboardView(LoginRequiredMixin, ListView):
    model = Sensor
    template_name = 'sensors/dashboard.html'
    context_object_name = 'sensors'
    login_url = 'accounts:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sensor_types'] = SensorType.objects.all()
        
        # Add external server status
        external_service = ExternalSensorService()
        is_available, server_info = external_service.check_external_server_health()
        context['external_server'] = {
            'is_available': is_available,
            'info': server_info,
            'url': external_service.base_url
        }
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by sensor type if provided
        sensor_type = self.request.GET.get('type')
        if sensor_type:
            try:
                type_id = int(sensor_type)
                queryset = queryset.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass
            
        return queryset

class SensorDetailView(LoginRequiredMixin, DetailView):
    model = Sensor
    template_name = 'sensors/detail.html'
    context_object_name = 'sensor'
    login_url = 'accounts:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the latest data for this sensor
        sensor = self.get_object()
        sensor_data = SensorData.objects.filter(sensor=sensor)
        
        context['latest_data'] = sensor_data.order_by('-timestamp').first()
        context['recent_data'] = sensor_data.order_by('-timestamp')[:10]
        
        # Add manual data entry form if user owns this sensor
        if self.request.user.is_authenticated and self.request.user == sensor.owner:
            context['data_form'] = ManualDataEntryForm()
        
        # Add statistics if data exists
        if sensor_data.exists():
            aggregates = sensor_data.aggregate(
                max_value=Max('value'),
                min_value=Min('value'),
                avg_value=Avg('value')
            )
            
            context['stats'] = {
                'max': aggregates['max_value'],
                'min': aggregates['min_value'],
                'avg': round(aggregates['avg_value'], 2) if aggregates['avg_value'] else 0,
                'count': sensor_data.count(),
                'unit': context['latest_data'].unit if context['latest_data'] else 'units'
            }
        else:
            # Generate some demo data for display
            demo_data = generate_demo_data(sensor, 1)[0]
            context['demo_data'] = demo_data
        
        return context

class SensorManageView(LoginRequiredMixin, ListView):
    model = Sensor
    template_name = 'sensors/manage.html'
    context_object_name = 'sensors'
    
    def get_queryset(self):
        return Sensor.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sensor_types'] = SensorType.objects.all()
        return context

class SensorCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Sensor
    template_name = 'sensors/form.html'
    form_class = SensorForm
    success_url = reverse_lazy('sensors:manage')
    success_message = "Sensor '%(sensor_id)s' was created successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Sensor'
        context['submit_text'] = 'Add Sensor'
        return context
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        
        # Save the sensor first
        response = super().form_valid(form)
        
        # Send sensor data to external server
        external_service = ExternalSensorService()
        success, result = external_service.send_sensor_to_external_server(self.object)
        
        if success:
            messages.success(self.request, f"Sensor '{self.object.sensor_id}' was also successfully registered on the external server.")
        else:
            messages.warning(self.request, f"Sensor '{self.object.sensor_id}' was created locally, but could not be sent to external server: {result.get('message', 'Unknown error')}")
        
        return response

class SensorEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Sensor
    template_name = 'sensors/form.html'
    form_class = SensorForm
    success_url = reverse_lazy('sensors:manage')
    success_message = "Sensor '%(sensor_id)s' was updated successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Sensor'
        context['submit_text'] = 'Update Sensor'
        return context
    
    def get_queryset(self):
        # Ensure users can only edit their own sensors
        return Sensor.objects.filter(owner=self.request.user)

class SensorDeleteView(LoginRequiredMixin, DeleteView):
    model = Sensor
    template_name = 'sensors/confirm_delete.html'
    success_url = reverse_lazy('sensors:manage')
    context_object_name = 'sensor'
    
    def get_queryset(self):
        # Ensure users can only delete their own sensors
        return Sensor.objects.filter(owner=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        """Override delete to also remove from external server"""
        self.object = self.get_object()
        sensor_id = self.object.sensor_id
        
        # Delete from external server first
        external_service = ExternalSensorService()
        success, result = external_service.delete_sensor_from_external_server(sensor_id)
        
        # Delete from local database
        response = super().delete(request, *args, **kwargs)
        
        if success:
            messages.success(request, f"Sensor '{sensor_id}' was successfully deleted from both local and external servers.")
        else:
            messages.warning(request, f"Sensor '{sensor_id}' was deleted locally, but could not be removed from external server: {result.get('message', 'Unknown error')}")
        
        return response

@login_required
def get_sensor_data(request, sensor_id):
    """API endpoint to get sensor data for charts"""
    sensor = get_object_or_404(Sensor, pk=sensor_id, owner=request.user)
    
    # Get time range from request or default to last 24 hours
    time_range = request.GET.get('range', '24h')
    
    # Get real data points based on time range
    data = SensorData.objects.filter(sensor=sensor).order_by('timestamp')
    
    # If no data exists, generate demo data
    if not data:
        demo_data_objects = []
        demo_data = generate_demo_data(sensor)
        
        for point in demo_data:
            demo_data_objects.append(type('DemoSensorData', (), {
                'timestamp': point['timestamp'],
                'value': point['value'],
                'unit': point['unit']
            }))
        
        # Use the demo data instead
        chart_data = prepare_time_series_data(demo_data_objects, time_range)
    else:
        # Use real data
        chart_data = prepare_time_series_data(data, time_range)
    
    # Add sensor info to the chart
    chart_data['sensor'] = {
        'name': sensor.name,
        'type': sensor.type.name,
        'location': sensor.location
    }
    
    return JsonResponse(chart_data)

@login_required
def add_sensor_data(request, sensor_id):
    """Add a manual data point to a sensor"""
    sensor = get_object_or_404(Sensor, pk=sensor_id, owner=request.user)
    
    if request.method == 'POST':
        form = ManualDataEntryForm(request.POST)
        
        if form.is_valid():
            data_point = form.save(commit=False)
            data_point.sensor = sensor
            data_point.save()
            
            # Send value update to external server
            external_service = ExternalSensorService()
            success, result = external_service.update_sensor_value(sensor, data_point.value, data_point.unit)
            
            if success:
                messages.success(request, f"Data point added successfully: {data_point.value} {data_point.unit}. External server updated.")
            else:
                messages.success(request, f"Data point added successfully: {data_point.value} {data_point.unit}")
                messages.warning(request, f"Could not update external server: {result.get('message', 'Unknown error')}")
            
            return redirect('sensors:detail', pk=sensor_id)
    
    # If form invalid or not POST, redirect back to detail page
    return redirect('sensors:detail', pk=sensor_id)
