"""
Collection of constants
"""
# flask server config
FLASK_PORT = 3307

# DB server config
DB_IP = '192.168.99.100'
DB_PORT = 31111
DB_USER = 'testuser'
DB_PASSWORD = 'testpassword'
DB_DATABASE = 'testdb'

# volume config
INPUT_MOUNT_PATH = '/input'
OUTPUT_MOUNT_PATH = '/output'

INPUT_HOST_PATH = '/hosthome/kjy/input/'  # Dataset 이 준비되어 있는 host 의 경로
OUTPUT_HOST_PATH = '/mnt/sda1/data/'  # 학습 결과를 저장할 host 의 경로

# model config
AE_MODEL_NAME = 'ae'
AE_MODEL_IMAGE_URL = '192.1.4.75:5000/model-ae:v0.1.9'

# k8s config
SERVICE_ACCOUNT_NAME = 'kjy'
