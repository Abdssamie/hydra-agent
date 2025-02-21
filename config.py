from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
DB_SCHEME = os.getenv('DB_SCHEME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')
MONGODB_URL = os.getenv('MONGODB_URL')
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
