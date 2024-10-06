from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')  # variable d'environnement email_user
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

DB_PASS = os.environ.get('DB_PASS')

