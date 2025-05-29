#!/usr/bin/env python
"""
Simple script to debug the external API 400 error
Run this from the project directory: python debug_external_api.py
"""

import os
import sys
import django
import json
import requests
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sensors.models import Sensor, SensorType
from django.contrib.auth.models import User

def sanitize_string(value):
    """Sanitize string values for FIWARE compatibility"""
    if not value:
        return "Unknown"
    
    # Replace problematic characters
    sanitized = str(value)
    sanitized = sanitized.replace("(", "_")
    sanitized = sanitized.replace(")", "_")
    sanitized = sanitized.replace(" ", "_")
    sanitized = sanitized.replace("ñ", "n")
    sanitized = sanitized.replace("á", "a")
    sanitized = sanitized.replace("é", "e")
    sanitized = sanitized.replace("í", "i")
    sanitized = sanitized.replace("ó", "o")
    sanitized = sanitized.replace("ú", "u")
    sanitized = sanitized.replace("Á", "A")
    sanitized = sanitized.replace("É", "E")
    sanitized = sanitized.replace("Í", "I")
    sanitized = sanitized.replace("Ó", "O")
    sanitized = sanitized.replace("Ú", "U")
    
    return sanitized

def test_external_api():
    """Test the external API with a sample sensor"""

    # Configuration
    base_url = "http://10.38.32.137:5026/v2/entities"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    print("=== External API Debug Tool ===")
    print(f"Target URL: {base_url}")
    print(f"Headers: {headers}")
    print()

    # Test 1: Check if server is reachable
    print("1. Testing server connectivity...")
    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        print(f"   Server response status: {response.status_code}")
        print(f"   Response headers: {dict(response.headers)}")
        if response.text:
            print(f"   Response body: {response.text[:200]}...")
        print()
    except requests.exceptions.ConnectionError:
        print("   ERROR: Cannot connect to server")
        return
    except Exception as e:
        print(f"   ERROR: {e}")
        return

    # Test 2: Try to get an existing sensor
    try:
        sensor = Sensor.objects.first()
        if not sensor:
            print("   No sensors found in database to test with")
            return

        print(f"2. Testing with sensor: {sensor.sensor_id} ({sensor.name})")
    except Exception as e:
        print(f"   ERROR getting sensor from database: {e}")
        return    # Test 3: Create payload
    print("3. Creating FIWARE NGSI payload...")
    sensor_data = {
        "id": sanitize_string(sensor.sensor_id),
        "type": "Sensor",
        "name": {
            "value": sanitize_string(sensor.name),
            "type": "Text"
        },
        "sensorType": {
            "value": sanitize_string(sensor.type.name),
            "type": "Text"
        },
        "parameter": {
            "value": sanitize_string(sensor.parameter),
            "type": "Text"
        },
        "location": {
            "value": sanitize_string(sensor.location),
            "type": "Text"
        },
        "owner": {
            "value": sanitize_string(sensor.owner.username),
            "type": "Text"
        },
        "isActive": {
            "value": sensor.is_active,
            "type": "Boolean"
        },
        "createdAt": {
            "value": sensor.created_at.isoformat() if sensor.created_at else datetime.now().isoformat(),
            "type": "DateTime"
        },
        "sensorValue": {
            "value": 0,
            "type": "Number",
            "metadata": {
                "unit": {
                    "value": "units",
                    "type": "Text"
                },
                "timestamp": {
                    "value": datetime.now().isoformat(),
                    "type": "DateTime"
                }
            }
        }
    }

    print("   Payload created:")
    print(json.dumps(sensor_data, indent=2))
    print()

    # Test 4: Send to external server
    print("4. Sending to external server...")
    try:
        response = requests.post(
            base_url,
            headers=headers,
            data=json.dumps(sensor_data),
            timeout=10
        )

        print(f"   Response Status: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")

        if response.text:
            print(f"   Response Body: {response.text}")

        if response.status_code == 400:
            print("\n   === 400 ERROR ANALYSIS ===")
            try:
                error_data = response.json()
                print(f"   Error Details: {json.dumps(error_data, indent=2)}")
            except Exception:
                print(f"   Raw Error Text: {response.text}")
        elif response.status_code in [200, 201, 204]:
            print("   SUCCESS: Sensor sent successfully!")
        else:
            print(f"   Unexpected status code: {response.status_code}")

    except Exception as e:
        print(f"   ERROR sending request: {e}")

    print("\n=== Debug Complete ===")

if __name__ == "__main__":
    test_external_api()
