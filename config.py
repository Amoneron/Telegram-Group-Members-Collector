#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID', '28636543'))
API_HASH = os.getenv('API_HASH', 'ac51c6ea25ee4796ce3772322211dfde')
SESSION_NAME = os.getenv('SESSION_NAME', 'telegram_session')

RESULTS_DIR = 'results'

SYSTEM_VERSION = "4.16.30-vxTL"
DEVICE_MODEL = "iOS"
APP_VERSION = "5.0.2"
LANG_CODE = "ru"

RATE_LIMIT_DELAY = 0.5
BATCH_SIZE = 100
MESSAGE_FETCH_LIMIT = 200
