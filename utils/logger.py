import logging
import os

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bibliotheque.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('bibliotheque') 