# Flask Endpoint Scheduler

A flexible Flask application that manages scheduled API endpoint calls with configurable timing and retry mechanisms.

## Features

- Schedule API endpoint calls using different patterns:
  - Fixed intervals (every X minutes)
  - Daily schedules (at specific times)
  - Weekly schedules (on specific days and times)
- Configurable retry mechanism for failed endpoint calls
- Environment-based configuration
- Thread-safe scheduler implementation
- Detailed logging

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your configuration:

```env
# Endpoint Configuration
TASK_ENDPOINT_URL=http://localhost:8000/api/task
TASK_METHOD=GET
TASK_AUTH_TOKEN=your-auth-token-here

# Schedule Configuration
TASK_SCHEDULE_TYPE=weekly  # Options: interval, daily, weekly
SCHEDULE_DAYS=1,3,5       # 0=Monday, 6=Sunday
SCHEDULE_TIME=14:30       # Time for daily/weekly schedules
SCHEDULER_INTERVAL_MINUTES=1  # For interval schedule type

# Retry Configuration
MAX_RETRIES=3
RETRY_DELAY=5
REQUEST_TIMEOUT=30

# Application Configuration
LOG_LEVEL=INFO
FLASK_PORT=8000
```

## Project Structure

```
├── app.py              # Main Flask application
├── endpoints.py        # Endpoint handling logic
├── scheduler.py        # Scheduler implementation
├── settings.py         # Configuration management
└── requirements.txt    # Project dependencies
```

## Usage

1. Start the application:
```bash
python app.py
```

2. The scheduler will automatically start in a background thread and begin making API calls according to your configuration.

3. Monitor the application logs for endpoint call results and any potential errors.

## Adding New Endpoints

To add new endpoints, update the `ENDPOINTS` dictionary in `settings.py`:

```python
ENDPOINTS = {
    'scheduled_task': {
        'url': os.getenv('TASK_ENDPOINT_URL'),
        'method': os.getenv('TASK_METHOD'),
        'headers': {
            'Authorization': os.getenv('TASK_AUTH_TOKEN'),
            'Content-Type': 'application/json'
        },
        'schedule': {
            'type': os.getenv('TASK_SCHEDULE_TYPE'),
            'interval_minutes': int(os.getenv('SCHEDULER_INTERVAL_MINUTES')),
            'days': [int(x) for x in os.getenv('SCHEDULE_DAYS').split(',')],
            'time': time.fromisoformat(os.getenv('SCHEDULE_TIME'))
        },
        'retry': {
            'max_attempts': int(os.getenv('MAX_RETRIES')),
            'delay_seconds': int(os.getenv('RETRY_DELAY'))
        }
    },
    'another_task': {
        # Add another endpoint configuration here
    }
}
```

## Error Handling

The application includes built-in error handling:
- Automatic retries for failed endpoint calls
- Configurable retry attempts and delays
- Detailed error logging
- Configuration validation at startup

## Requirements

- Python 3.7+
- Flask
- python-dotenv
- schedule
- requests

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
