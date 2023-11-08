from dotenv import load_dotenv
import os
from pathlib import Path
import requests
import json
from datetime import datetime
from datetime import timedelta
from typing import Optional, Union

# Load .env file
ROOT_DIR = Path(__file__).parent.parent
dotenv_file = ROOT_DIR / '.env'
load_dotenv(dotenv_file)

# base url + endpoints
base_url = "https://api.plaato.cloud/"
devices_endpoint = "devices"

# Get API key from .env file
api_key = os.getenv("PLAATO_KEY")
header_param = {"x-plaato-api-key": api_key}

def get_all_devices(print_data: bool=False, ids_only: bool=False) -> Union[list[str], dict]:
    # Display all devices data
    print(f"Fetching all devices data from {base_url}...")
    try:
        response = requests.get(base_url + devices_endpoint, headers=header_param)
        devices_data = response.json()
        if print_data:
            print(json.dumps(devices_data, indent=4, sort_keys=True))
        # Fetching ids only
        if ids_only:
            devices_id = [device["id"] for device in devices_data]
            return devices_id
        return json.dumps(devices_data, indent=2)
    except Exception as e:
        print(f"Error fetching devices data: {e}")
        return []

def get_readings_from_single_device(
    device_id: str, 
    start_date: Optional[int]=None, 
    end_date: Optional[datetime]=None
) -> list[dict]:
    # Set defaults from time params
    if start_date is None:
        start_date = datetime.now() - timedelta(days=7)
    if end_date is None:
        end_date = datetime.now()
    period = end_date - start_date
    print(
        f"Fetching readings from {device_id=}\n" 
        f"{datetime.strftime(start_date, '%d-%m-%Y %I:%M %p')} to "
        f"{datetime.strftime(end_date, '%d-%m-%Y %I:%M %p')} ({period.days} days):"
    )
    
    # Setting query params
    params = {
        "temperatureUnit": "Celsius",
        "densityUnit": "Plato",
        "from": start_date.isoformat(),
        "to": end_date.isoformat()
    }
    
    # Get the readings data for the given time period
    readings_endpoint = f"{devices_endpoint}/{device_id}/readings"
    response = requests.get(
        base_url + readings_endpoint, 
        headers=header_param,
        params=params)
    readings = response.json()
    return json.dumps(readings, indent=2)
    
if __name__ == "__main__":
    # Get all devices
    devices_id = get_all_devices(print_data=True, ids_only=True)
    
    # Test latest readings with first device
    if len(devices_id) > 0:
        first_device = devices_id[0]
        first_device_readings = get_readings_from_single_device(device_id=first_device)
        print(first_device_readings)
        exit(0)
    else:
        print("No devices found")
        exit(1)
    
    
