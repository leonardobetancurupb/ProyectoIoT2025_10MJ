import os
import requests
import json
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_orion_url():
    """Get the Orion Context Broker URL from settings"""
    return settings.ORION_URL

def get_crate_url():
    """Get the CrateDB URL from settings"""
    return settings.CRATE_URL

def get_quantumleap_url():
    """Get the QuantumLeap URL from settings"""
    return settings.QUANTUMLEAP_URL

def get_entity_list():
    """
    Get list of all entities from Orion Context Broker
    """
    try:
        orion_url = get_orion_url()
        response = requests.get(f"{orion_url}/v2/entities", 
                               headers={"Accept": "application/json"})
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get entities: {response.status_code}, {response.text}")
            return []
    except Exception as e:
        logger.error(f"Exception when getting entities: {str(e)}")
        return []

def get_entity_by_id(entity_id):
    """
    Get entity by ID from Orion Context Broker
    """
    try:
        orion_url = get_orion_url()
        response = requests.get(f"{orion_url}/v2/entities/{entity_id}", 
                                headers={"Accept": "application/json"})
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get entity {entity_id}: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logger.error(f"Exception when getting entity {entity_id}: {str(e)}")
        return None

def create_entity(entity_data):
    """
    Create a new entity in Orion Context Broker
    """
    try:
        orion_url = get_orion_url()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.post(f"{orion_url}/v2/entities", 
                                 headers=headers,
                                 data=json.dumps(entity_data))
        if response.status_code == 201:
            return True
        else:
            logger.error(f"Failed to create entity: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception when creating entity: {str(e)}")
        return False

def update_entity(entity_id, entity_data):
    """
    Update an entity in Orion Context Broker
    """
    try:
        orion_url = get_orion_url()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.patch(f"{orion_url}/v2/entities/{entity_id}/attrs", 
                                  headers=headers,
                                  data=json.dumps(entity_data))
        if response.status_code == 204:
            return True
        else:
            logger.error(f"Failed to update entity {entity_id}: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception when updating entity {entity_id}: {str(e)}")
        return False

def delete_entity(entity_id):
    """
    Delete an entity from Orion Context Broker
    """
    try:
        orion_url = get_orion_url()
        response = requests.delete(f"{orion_url}/v2/entities/{entity_id}")
        if response.status_code == 204:
            return True
        else:
            logger.error(f"Failed to delete entity {entity_id}: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception when deleting entity {entity_id}: {str(e)}")
        return False

def get_historical_data(entity_id, entity_type, attribute, from_date=None, to_date=None):
    """
    Get historical data from QuantumLeap for a specific entity and attribute
    """
    try:
        quantumleap_url = get_quantumleap_url()
        params = {
            "type": entity_type,
            "limit": 100,
        }
        
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
            
        response = requests.get(
            f"{quantumleap_url}/v2/entities/{entity_id}/attrs/{attribute}",
            params=params
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get historical data: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        logger.error(f"Exception when getting historical data: {str(e)}")
        return None
