import json
import requests
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class ExternalSensorService:
    """Service to handle sensor data synchronization with external server"""
    
    def __init__(self):
        self.base_url = "http://10.38.32.137:5026/v2/entities"
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def _sanitize_string(self, value):
        """
        Sanitize string values for FIWARE compatibility
        Remove or replace invalid characters
        """
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
    
    def send_sensor_to_external_server(self, sensor):
        """
        Send sensor data to external server when a sensor is created
        
        Args:
            sensor: Sensor model instance
            
        Returns:
            tuple: (success: bool, response_data: dict)
        """
        try:
            # Prepare sensor data in FIWARE/NGSI format
            sensor_data = {
                "id": self._sanitize_string(sensor.sensor_id),
                "type": "Sensor",
                "name": {
                    "value": self._sanitize_string(sensor.name),
                    "type": "Text"
                },
                "sensorType": {
                    "value": self._sanitize_string(sensor.type.name),
                    "type": "Text"
                },
                "parameter": {
                    "value": self._sanitize_string(sensor.parameter),
                    "type": "Text"
                },
                "location": {
                    "value": self._sanitize_string(sensor.location),
                    "type": "Text"
                },
                "owner": {
                    "value": self._sanitize_string(sensor.owner.username),
                    "type": "Text"
                },
                "isActive": {
                    "value": sensor.is_active,
                    "type": "Boolean"
                },
                "createdAt": {
                    "value": sensor.created_at.isoformat() if sensor.created_at else timezone.now().isoformat(),
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
                            "value": timezone.now().isoformat(),
                            "type": "DateTime"
                        }
                    }
                }
            }
            
            logger.info(f"Sending sensor {sensor.sensor_id} to external server")
            logger.debug(f"Payload: {json.dumps(sensor_data, indent=2)}")
            
            # Send POST request to external server
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(sensor_data),
                timeout=10
            )
            
            if response.status_code in [200, 201, 204]:
                logger.info(f"Successfully sent sensor {sensor.sensor_id} to external server")
                return True, {"status": "success", "message": "Sensor sent to external server"}
            else:
                error_details = f"Status: {response.status_code}"
                try:
                    error_response = response.json()
                    error_details += f", Error: {error_response}"
                except:
                    error_details += f", Response: {response.text}"
                
                logger.error(f"Failed to send sensor {sensor.sensor_id}. {error_details}")
                return False, {"status": "error", "message": f"External server error - {error_details}"}
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout sending sensor {sensor.sensor_id} to external server")
            return False, {"status": "error", "message": "Timeout connecting to external server"}
            
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error sending sensor {sensor.sensor_id} to external server")
            return False, {"status": "error", "message": "Could not connect to external server"}
            
        except Exception as e:
            logger.error(f"Unexpected error sending sensor {sensor.sensor_id}: {str(e)}")
            return False, {"status": "error", "message": f"Unexpected error: {str(e)}"}
    
    def update_sensor_value(self, sensor, value, unit="units"):
        """
        Update sensor value on external server
        
        Args:
            sensor: Sensor model instance
            value: The sensor reading value
            unit: The unit of measurement
            
        Returns:
            tuple: (success: bool, response_data: dict)
        """
        try:
            # Prepare value update data
            update_data = {
                "sensorValue": {
                    "value": value,
                    "type": "Number",
                    "metadata": {
                        "unit": {
                            "value": unit,
                            "type": "Text"
                        },
                        "timestamp": {
                            "value": timezone.now().isoformat(),
                            "type": "DateTime"
                        }
                    }
                }
            }
            
            # Update existing entity
            url = f"{self.base_url}/{self._sanitize_string(sensor.sensor_id)}/attrs"
            response = requests.patch(
                url,
                headers=self.headers,
                data=json.dumps(update_data),
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                logger.info(f"Successfully updated sensor {sensor.sensor_id} value on external server")
                return True, {"status": "success", "message": "Sensor value updated on external server"}
            else:
                logger.error(f"Failed to update sensor {sensor.sensor_id} value. Status: {response.status_code}")
                return False, {"status": "error", "message": f"External server returned status {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Error updating sensor {sensor.sensor_id} value: {str(e)}")
            return False, {"status": "error", "message": f"Error updating value: {str(e)}"}
    
    def delete_sensor_from_external_server(self, sensor_id):
        """
        Delete sensor from external server
        
        Args:
            sensor_id: The sensor ID to delete
            
        Returns:
            tuple: (success: bool, response_data: dict)
        """
        try:
            url = f"{self.base_url}/{self._sanitize_string(sensor_id)}"
            response = requests.delete(url, headers=self.headers, timeout=10)
            
            if response.status_code in [200, 204]:
                logger.info(f"Successfully deleted sensor {sensor_id} from external server")
                return True, {"status": "success", "message": "Sensor deleted from external server"}
            else:
                logger.error(f"Failed to delete sensor {sensor_id}. Status: {response.status_code}")
                return False, {"status": "error", "message": f"External server returned status {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Error deleting sensor {sensor_id}: {str(e)}")
            return False, {"status": "error", "message": f"Error deleting sensor: {str(e)}"}
    
    def check_external_server_health(self):
        """
        Check if external server is reachable
        
        Returns:
            tuple: (is_available: bool, response_info: dict)
        """
        try:
            # Try to access the base API endpoint
            response = requests.get(
                self.base_url.replace('/v2/entities', '/version'),
                headers=self.headers,
                timeout=5
            )
            
            if response.status_code == 200:
                return True, {"status": "online", "message": "External server is reachable"}
            else:
                # Try just the entities endpoint
                response = requests.get(self.base_url, headers=self.headers, timeout=5)
                if response.status_code in [200, 400]:
                    return True, {"status": "online", "message": "External server is reachable"}
                else:
                    return False, {"status": "error", "message": f"Server returned status {response.status_code}"}
                    
        except requests.exceptions.Timeout:
            return False, {"status": "timeout", "message": "External server timeout"}
        except requests.exceptions.ConnectionError:
            return False, {"status": "offline", "message": "Cannot connect to external server"}
        except Exception as e:
            return False, {"status": "error", "message": f"Error checking server: {str(e)}"}
