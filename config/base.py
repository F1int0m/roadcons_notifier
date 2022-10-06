import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOT_TOKEN = '123'

DB_NAME = 'roadcons'
DB_USER = 'roadcons'
DB_PASS = 'change'

DB_HOST = 'localhost'
DB_PORT = 5432

# Google API config
API_KEY = '123'
DISCOVERY_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

DEFAULT_JOB_NAME = 'Update_projects_job'
JOB_UPDATE_INTERVAL = 60 * 20  # в секундах
NOTIFICATION_DELAY = 10
