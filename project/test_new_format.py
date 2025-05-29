
"""
Debug script to test the new simplified format for external API
"""
import requests
import json

base_url = "http://10.38.32.137:5026/v2/entities"
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def test_simplified_format():
    """Test the new simplified format as requested by user"""
    
    
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

if __name__ == "__main__":
    print("Testing new simplified format for external server...")
    success = test_simplified_format()
    print(f"\nResult: {'✓ SUCCESS' if success else '✗ FAILED'}")
