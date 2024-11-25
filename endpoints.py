import logging
import requests
import settings

logger = logging.getLogger(__name__)

class EndpointHandler:
    def __init__(self, endpoint_name, config):
        self.endpoint_name = endpoint_name
        self.config = config
        self.url = config['url']
        self.method = config['method']
        self.headers = config.get('headers', {})
        self.retry_config = config['retry']
        
    def execute(self):
        for attempt in range(self.retry_config['max_attempts']):
            try:
                response = requests.request(
                    method=self.method,
                    url=self.url,
                    headers=self.headers,
                    timeout=settings.REQUEST_TIMEOUT
                )
                response.raise_for_status()
                logger.info(f"Endpoint {self.endpoint_name} called successfully: {response.text}")
                return response
                
            except Exception as e:
                logger.error(f"Error calling endpoint {self.endpoint_name} (attempt {attempt + 1}): {e}")
                if attempt < self.retry_config['max_attempts'] - 1:
                    time.sleep(self.retry_config['delay_seconds'])
                else:
                    logger.error(f"Max retries reached for endpoint {self.endpoint_name}")
                    raise