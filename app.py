import logging
import settings
from flask import Flask
from dotenv import load_dotenv
import threading
import schedule
import time
from scheduler import start_scheduler

load_dotenv()

# Set up logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler in a background thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True  # Daemon threads exit when the main program exits
scheduler_thread.start()

# Initialize the scheduler
start_scheduler()

@app.route('/')
def home():
    return "Scheduler Test App"

if __name__ == '__main__':
    logger.info(f"Starting Flask app on port {settings.FLASK_PORT}")
    app.run(host='0.0.0.0', port=settings.FLASK_PORT, debug=False)