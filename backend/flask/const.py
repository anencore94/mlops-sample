"""
Collection of constants
"""
import os
# flask server config
FLASK_PORT = 3307

# DB server config
DB_IP = os.getenv('DB_IP')
DB_PORT = int(os.getenv('DB_PORT'))
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

# volume config
INPUT_MOUNT_PATH = '/input'
OUTPUT_MOUNT_PATH = '/output'

# model config
AE_MODEL_NAME = 'ae'
AE_MODEL_IMAGE_URL = os.getenv('AE_MODEL_IMAGE_URL')

# k8s config
SERVICE_ACCOUNT_NAME = 'kjy'
