import logging
import os
from datetime import datetime

# Create logs directory
LOG_DIR = "logs"
LOG_PATH = os.path.join(os.getcwd(), LOG_DIR)
os.makedirs(LOG_PATH, exist_ok=True)

# Create log file name with timestamp
CURRENT_TIME_STAMP = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
file_name = f"log_{CURRENT_TIME_STAMP}.log"

# Full path of log file
log_file_path = os.path.join(LOG_PATH, file_name)

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    filemode="a",  # better than "w"
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Test log
logging.info("Logging setup complete")