"""
Collection of constants
"""
# server config
FLASK_PORT = "3307"

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