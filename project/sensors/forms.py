from django import forms
from .models import SensorType, Sensor, SensorData

class SensorForm(forms.ModelForm):
    """Form for creating and updating sensors"""
    class Meta:
        model = Sensor
        fields = ['name', 'type', 'location', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter sensor name'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where is this sensor located?'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

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
