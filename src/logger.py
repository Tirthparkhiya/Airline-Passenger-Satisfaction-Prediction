import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

# Generate a unique log file name using timestamp (date + time)
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Configure basic logging settings
logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

"""
This logs messages with level INFO and higher:
1. CRITICAL
2. ERROR
3. WARNING
4. INFO
(5. DEBUG is lower and will not be shown with INFO level)
"""

# Logger getter function
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
