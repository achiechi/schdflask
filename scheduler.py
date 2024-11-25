import logging
import schedule
from datetime import datetime
from endpoints import EndpointHandler
import settings

logger = logging.getLogger(__name__)

def setup_job(endpoint_name, config):
    handler = EndpointHandler(endpoint_name, config)
    
    if config['schedule']['type'] == 'interval':
        schedule.every(config['schedule']['interval_minutes']).minutes.do(handler.execute)
        logger.info(f"Scheduled {endpoint_name} to run every {config['schedule']['interval_minutes']} minutes")
        
    elif config['schedule']['type'] == 'daily':
        schedule.every().day.at(config['schedule']['time'].strftime('%H:%M')).do(handler.execute)
        logger.info(f"Scheduled {endpoint_name} to run daily at {config['schedule']['time']}")
        
    elif config['schedule']['type'] == 'weekly':
        for day in config['schedule']['days']:
            schedule_time = config['schedule']['time'].strftime('%H:%M')
            getattr(schedule.every(), schedule.weekday[day]).at(schedule_time).do(handler.execute)
        logger.info(f"Scheduled {endpoint_name} to run weekly on days {config['schedule']['days']} at {config['schedule']['time']}")

def start_scheduler():
    for endpoint_name, config in settings.ENDPOINTS.items():
        setup_job(endpoint_name, config)
    logger.info("All endpoints scheduled successfully")