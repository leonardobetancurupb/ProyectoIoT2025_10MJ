#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    print("Attempting to import ExternalSensorService...")
    from sensors.external_service import ExternalSensorService
    print("✓ Import successful!")
    
    # Test instantiation
    service = ExternalSensorService()
    print("✓ Service instance created successfully!")
    
    # Test health check method
    is_available, info = service.check_external_server_health()
    print(f"✓ Health check method works: {info}")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")
    
    # Let's check if the file exists and has content
    import os
    file_path = os.path.join(os.path.dirname(__file__), 'sensors', 'external_service.py')
    print(f"File path: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
            print(f"File size: {len(content)} characters")
            print(f"First 200 characters: {content[:200]}")
            
except Exception as e:
    print(f"✗ Other error: {e}")
