from django import forms
from .models import SensorType, Sensor, SensorData

class SensorForm(forms.ModelForm):
    """Form for creating and updating sensors"""
    sensor_id = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter unique sensor ID (e.g., TEMP_001)',
            'required': True
        }),
        help_text="A unique identifier for your sensor"
    )
    
    parameter = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter parameter name (e.g., temperature, humidity)',
            'required': True
        }),
        help_text="What does this sensor measure?"
    )
    
    class Meta:
        model = Sensor
        fields = ['sensor_id', 'type', 'parameter']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].help_text = "Select the type of sensor"
        
    def save(self, commit=True):
        sensor = super().save(commit=False)
        # Auto-generate name from sensor_id and parameter
        sensor.name = f"{sensor.sensor_id} ({sensor.parameter})"
        if commit:
            sensor.save()
        return sensor

class SensorTypeForm(forms.ModelForm):
    """Form for creating and updating sensor types"""
    class Meta:
        model = SensorType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter type name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe this sensor type'}),
        }

class SensorFilterForm(forms.Form):
    """Form for filtering sensors on dashboard"""
    type = forms.ModelChoiceField(
        queryset=SensorType.objects.all(),
        required=False,
        empty_label="All Sensor Types",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status'), ('active', 'Active Only'), ('inactive', 'Inactive Only')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class ManualDataEntryForm(forms.ModelForm):
    """Form for manually entering sensor data"""
    class Meta:
        model = SensorData
        fields = ['value', 'unit']
        widgets = {
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
        }
