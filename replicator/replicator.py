#!/usr/bin/env python
"""
Replicator Service for ProyectoIoT2025_10MJ

This service polls the Orion Context Broker for specified entity types and
replicates the data to a local SQLite database for use by the Django application.
"""

import os
import sys
import time
import json
import logging
import sqlite3
import requests
import schedule
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("replicator")

# Read configuration from environment variables
ORION_URL = os.environ.get('ORION_URL', 'http://orion:1026')
DB_PATH = os.environ.get('DJANGO_DB_URL', 'sqlite:////app/db.sqlite3').replace('sqlite:///', '')
POLL_INTERVAL = int(os.environ.get('POLL_INTERVAL', '300'))  # Default: 5 minutes
ENTITY_TYPES = os.environ.get('ENTITY_TYPES', 'Sensor,Device,EnvironmentalReading').split(',')

# Constants
API_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

class OrionReplicator:
    def __init__(self):
        self.orion_url = ORION_URL
        self.db_path = DB_PATH
        logger.info(f"Initialized with Orion URL: {self.orion_url}, DB path: {self.db_path}")
        logger.info(f"Entity types to replicate: {ENTITY_TYPES}")
        logger.info(f"Polling interval: {POLL_INTERVAL} seconds")
        
        # Ensure DB tables exist
        self.init_db()

    def init_db(self):
        """Initialize database tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if sensors_sensor table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sensors_sensor (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    entity_type TEXT,
                    location TEXT,
                    description TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            """)
            
            # Check if sensors_sensorreading table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sensors_sensorreading (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sensor_id TEXT,
                    value REAL,
                    unit TEXT,
                    timestamp TIMESTAMP,
                    FOREIGN KEY (sensor_id) REFERENCES sensors_sensor(id)
                )
            """)
            
            conn.commit()
            logger.info("Database tables initialized")
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
        finally:
            if conn:
                conn.close()

    def get_entities(self, entity_type):
        """Get entities of a specific type from Orion Context Broker"""
        for attempt in range(MAX_RETRIES):
            try:
                url = f"{self.orion_url}/v2/entities"
                params = {'type': entity_type, 'limit': 1000}
                headers = {'Accept': 'application/json'}
                
                response = requests.get(url, params=params, headers=headers, timeout=API_TIMEOUT)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"Failed to get entities: {response.status_code}, {response.text}")
                    
            except requests.RequestException as e:
                logger.error(f"Request error: {e}")
                
            # If we get here, there was an error - wait and retry
            if attempt < MAX_RETRIES - 1:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
                
        logger.error(f"Failed to get entities after {MAX_RETRIES} attempts")
        return []

    def process_sensor_entity(self, entity):
        """Process a sensor entity and save to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            entity_id = entity.get('id', '')
            entity_type = entity.get('type', '')
            
            # Extract common attributes with fallbacks
            name = entity.get('name', {}).get('value', entity_id)
            location = entity.get('location', {}).get('value', 'Unknown')
            description = entity.get('description', {}).get('value', '')
            
            now = datetime.now().isoformat()
            
            # Check if sensor exists
            cursor.execute("SELECT id FROM sensors_sensor WHERE id = ?", (entity_id,))
            exists = cursor.fetchone()
            
            if exists:
                # Update existing sensor
                cursor.execute("""
                    UPDATE sensors_sensor 
                    SET name = ?, location = ?, description = ?, updated_at = ?
                    WHERE id = ?
                """, (name, location, description, now, entity_id))
                logger.info(f"Updated sensor: {entity_id}")
            else:
                # Insert new sensor
                cursor.execute("""
                    INSERT INTO sensors_sensor (id, name, entity_type, location, description, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (entity_id, name, entity_type, location, description, now, now))
                logger.info(f"Created new sensor: {entity_id}")
            
            # Process readings if available
            self.process_sensor_readings(cursor, entity)
            
            conn.commit()
            
        except sqlite3.Error as e:
            logger.error(f"Database error for entity {entity_id}: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def process_sensor_readings(self, cursor, entity):
        """Process and store sensor readings"""
        sensor_id = entity.get('id', '')
        
        # Check for common measurement attributes
        for attr_name in ['temperature', 'humidity', 'pressure', 'luminosity', 'co2', 'value', 'measurement']:
            if attr_name in entity:
                try:
                    value = float(entity[attr_name].get('value', 0))
                    unit = entity[attr_name].get('metadata', {}).get('unitCode', {}).get('value', '')
                    timestamp = datetime.now().isoformat()
                    
                    # Store the reading
                    cursor.execute("""
                        INSERT INTO sensors_sensorreading (sensor_id, value, unit, timestamp)
                        VALUES (?, ?, ?, ?)
                    """, (sensor_id, value, unit, timestamp))
                    logger.debug(f"Stored reading for {sensor_id}: {value} {unit}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid reading for {sensor_id}.{attr_name}: {e}")

    def sync(self):
        """Main synchronization function"""
        logger.info("Starting synchronization with Orion Context Broker...")
        
        for entity_type in ENTITY_TYPES:
            logger.info(f"Retrieving entities of type: {entity_type}")
            entities = self.get_entities(entity_type)
            logger.info(f"Retrieved {len(entities)} entities of type {entity_type}")
            
            for entity in entities:
                self.process_sensor_entity(entity)
                
        logger.info("Synchronization completed")

    def run(self):
        """Run the replicator service"""
        logger.info("Starting Orion Replicator service")
        
        # Initial sync at startup
        self.sync()
        
        # Schedule regular syncs
        schedule.every(POLL_INTERVAL).seconds.do(self.sync)
        
        # Main loop
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    replicator = OrionReplicator()
    replicator.run()
