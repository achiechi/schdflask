import os
from datetime import time

# Endpoint Configuration
ENDPOINTS = {
    'scheduled_task': {  #your endpoint task
        'url': os.getenv('TASK_ENDPOINT_URL', 'http://localhost:8000/api/task'),
        'method': os.getenv('TASK_METHOD', 'GET'),
        'headers': {
            'Authorization': os.getenv('TASK_AUTH_TOKEN', ''),
            'Content-Type': 'application/json'
        },
        'schedule': {
            'type': os.getenv('TASK_SCHEDULE_TYPE', 'interval'),  # 'interval', 'daily', 'weekly'
            'interval_minutes': int(os.getenv('SCHEDULER_INTERVAL_MINUTES', '1')),
            'days': [int(x) for x in os.getenv('SCHEDULE_DAYS', '0,1,2,3,4,5,6').split(',')],  # 0 = Monday
            'time': time.fromisoformat(os.getenv('SCHEDULE_TIME', '09:00'))  # Daily/Weekly schedule time
        },
        'retry': {
            'max_attempts': int(os.getenv('MAX_RETRIES', '3')),
            'delay_seconds': int(os.getenv('RETRY_DELAY', '5'))
        }
    }
    # Add more endpoints as needed using the same pattern:
    # 'another_task': { ... }
}

# General Configuration
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
FLASK_PORT = int(os.getenv('FLASK_PORT', '8000'))

# Validate configuration
def validate_config():
    for endpoint_name, config in ENDPOINTS.items():
        required_fields = ['url', 'method', 'schedule', 'retry']
        missing = [f for f in required_fields if f not in config]
        if missing:
            raise ValueError(f"Endpoint {endpoint_name} missing required fields: {missing}")
        
        schedule = config['schedule']
        if schedule['type'] not in ['interval', 'daily', 'weekly']:
            raise ValueError(f"Invalid schedule type for {endpoint_name}: {schedule['type']}")
        
        if schedule['type'] in ['daily', 'weekly'] and not isinstance(schedule['time'], time):
            raise ValueError(f"Invalid time format for {endpoint_name}")
            
        if schedule['type'] == 'weekly' and not schedule['days']:
            raise ValueError(f"Weekly schedule for {endpoint_name} must specify days")

validate_config()