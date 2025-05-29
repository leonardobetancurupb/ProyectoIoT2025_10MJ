from django.core.management.base import BaseCommand
from sensors.models import Sensor
from sensors.external_service import ExternalSensorService

class Command(BaseCommand):
    help = 'Sync existing sensors to external server'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be synced without actually doing it',
        )
        parser.add_argument(
            '--sensor-id',
            type=str,
            help='Sync only a specific sensor by ID',
        )
    
    def handle(self, *args, **options):
        external_service = ExternalSensorService()
        
        if options['sensor_id']:
            # Sync specific sensor
            try:
                sensor = Sensor.objects.get(sensor_id=options['sensor_id'])
                sensors = [sensor]
            except Sensor.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Sensor with ID "{options["sensor_id"]}" not found')
                )
                return
        else:
            # Sync all sensors
            sensors = Sensor.objects.all()
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would sync {sensors.count()} sensors to external server')
            )
            for sensor in sensors:
                self.stdout.write(f'  - {sensor.sensor_id}: {sensor.name}')
            return
        
        successful = 0
        failed = 0
        
        for sensor in sensors:
            self.stdout.write(f'Syncing sensor: {sensor.sensor_id}...', ending='')
            
            success, result = external_service.send_sensor_to_external_server(sensor)
            
            if success:
                self.stdout.write(self.style.SUCCESS(' SUCCESS'))
                successful += 1
            else:
                self.stdout.write(self.style.ERROR(f' FAILED: {result.get("message", "Unknown error")}'))
                failed += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSync completed: {successful} successful, {failed} failed'
            )
        )
