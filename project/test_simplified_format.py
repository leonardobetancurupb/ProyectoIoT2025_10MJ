#!/usr/bin/env python3
"""
Debug script to test the new simplified format for external API
"""
import requests
import json

# External server configuration
base_url = "http://10.38.32.137:5026/v2/entities"
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def test_simplified_format():
    """Test the new simplified format as requested by user"""
    
    # Test data in the new simplified format
    sensor_data = {
        "id": "sensor_w_ht_001",
        "type": "humedad",
        "25.9": {
            "type": "Float",
            "value": 24.5,
            "metadata": {}
        }
    }
    
    print("=== Testing Simplified Format ===")
    print(f"Payload: {json.dumps(sensor_data, indent=2)}")
    
    try:
        response = requests.post(
            base_url,
            headers=headers,
            data=json.dumps(sensor_data),
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201, 204]:
            print("✓ SUCCESS: Sensor data sent successfully!")
            return True
        else:
            print(f"✗ ERROR: Status {response.status_code}")
            try:
                error_response = response.json()
                print(f"Error details: {error_response}")
            except:
                print(f"Response text: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ EXCEPTION: {e}")
        return False

def test_update_value():
    """Test updating a value with simplified format"""
    
    # Update data - just the new attribute
    update_data = {
        "30.2": {
            "type": "Float", 
            "value": 28.1,
            "metadata": {}
        }
    }
    
    print("\n=== Testing Value Update ===")
    print(f"Update payload: {json.dumps(update_data, indent=2)}")
    
    try:
        url = f"{base_url}/sensor_w_ht_001/attrs"
        response = requests.patch(
            url,
            headers=headers,
            data=json.dumps(update_data),
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print("✓ SUCCESS: Value updated successfully!")
            return True
        else:
            print(f"✗ ERROR: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ EXCEPTION: {e}")
        return False

if __name__ == "__main__":
    print("Testing new simplified format for external server...")
    
    # Test creation
    success1 = test_simplified_format()
    
    # Test update if creation was successful
    if success1:
        success2 = test_update_value()
    else:
        success2 = False
    
    print(f"\n=== SUMMARY ===")
    print(f"Creation: {'✓' if success1 else '✗'}")
    print(f"Update: {'✓' if success2 else '✗'}")
