from django.core.management.base import BaseCommand
from sensors.models import Sensor
from sensors.external_service import ExternalSensorService
import json
import logging

# Set up logging to see debug messages
logging.basicConfig(level=logging.DEBUG)

class Command(BaseCommand):
    help = 'Test external server API call with detailed debugging'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--sensor-id',
            type=str,
            help='Test with a specific sensor ID',
            required=True
        )
        parser.add_argument(
            '--show-payload',
            action='store_true',
            help='Show the exact payload being sent',
        )
    
    def handle(self, *args, **options):
        try:
            sensor = Sensor.objects.get(sensor_id=options['sensor_id'])
        except Sensor.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Sensor with ID "{options["sensor_id"]}" not found')
            )
            return
        
        self.stdout.write(f'Testing external API call for sensor: {sensor.sensor_id}')
        self.stdout.write(f'Sensor details:')
        self.stdout.write(f'  - Name: {sensor.name}')
        self.stdout.write(f'  - Type: {sensor.type.name}')
        self.stdout.write(f'  - Parameter: {sensor.parameter}')
        self.stdout.write(f'  - Location: {sensor.location}')
        self.stdout.write(f'  - Owner: {sensor.owner.username}')
        self.stdout.write(f'  - Active: {sensor.is_active}')
        
        external_service = ExternalSensorService()
        
        if options['show_payload']:
            # Show what would be sent
            sensor_data = {
                "id": sensor.sensor_id,
                "type": "Sensor",
                "name": {
                    "value": sensor.name,
                    "type": "Text"
                },
                "sensorType": {
                    "value": sensor.type.name,
                    "type": "Text"
                },
                "parameter": {
                    "value": sensor.parameter,
                    "type": "Text"
                },
                "location": {
                    "value": sensor.location or "Unknown",
                    "type": "Text"
                },
                "owner": {
                    "value": sensor.owner.username,
                    "type": "Text"
                },
                "isActive": {
                    "value": sensor.is_active,
                    "type": "Boolean"
                },
                "createdAt": {
                    "value": sensor.created_at.isoformat() if sensor.created_at else "2025-05-29T00:00:00",
                    "type": "DateTime"
                },
                "value": {
                    "value": 0,
                    "type": "Number",
                    "metadata": {
                        "unit": {
                            "value": "units",
                            "type": "Text"
                        },
                        "timestamp": {
                            "value": "2025-05-29T00:00:00",
                            "type": "DateTime"
                        }
                    }
                }
            }
            
            self.stdout.write('\nPayload that will be sent:')
            self.stdout.write(json.dumps(sensor_data, indent=2))
            self.stdout.write(f'\nTarget URL: {external_service.base_url}')
        
        self.stdout.write('\nSending to external server...')
        success, result = external_service.send_sensor_to_external_server(sensor)
        
        if success:
            self.stdout.write(self.style.SUCCESS('SUCCESS: Sensor sent successfully'))
        else:
            self.stdout.write(self.style.ERROR(f'FAILED: {result.get("message", "Unknown error")}'))
            self.stdout.write('\nTroubleshooting tips:')
            self.stdout.write('1. Check if the external server is running')
            self.stdout.write('2. Verify the URL is correct: http://10.38.32.137:5026/v2/entities')
            self.stdout.write('3. Check if the server accepts FIWARE NGSI format')
            self.stdout.write('4. Verify network connectivity to 10.38.32.137:5026')
