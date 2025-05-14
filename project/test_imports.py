"""
Test script to verify that the math module is properly imported.
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Try importing the modules with the fixed code
from sensors.utils import generate_demo_data
print("Successfully imported generate_demo_data from sensors.utils")

# Create a dummy class to test the function
class DummySensor:
    class DummyType:
        name = "temperature"
    
    type = DummyType()

# Try using the function that requires math
try:
    dummy_sensor = DummySensor()
    data = generate_demo_data(dummy_sensor, num_points=5)
    print("Successfully generated demo data")
    print(f"Generated {len(data)} data points")
    print(f"First data point: {data[0]}")
except Exception as e:
    print(f"Error generating demo data: {e}")

# Test data_init.py module
print("\nTesting data_init.py module:")
try:
    import data_init
    print("Successfully imported data_init module")
except Exception as e:
    print(f"Error importing data_init module: {e}")
