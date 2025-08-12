import os
from dotenv import load_dotenv
import time
from datetime import datetime, time
import rsa

load_dotenv()


ENV = 'dev'
# load_dotenv('.env', override=True)
if ENV == 'dev':
    print("Using '.env'")
    load_dotenv('.env', override=True)


DATABASE_URI = os.environ.get("DATABASE_URI")

ACCESS_TOKEN_SECRET_KEY = os.environ.get("ACCESS_TOKEN_SECRET_KEY")
ACCESS_TOKEN_ADMIN = os.environ.get("ACCESS_TOKEN_ADMIN")
AESCIPHER_SECRET_KEY =os.environ.get("AESCIPHER_SECRET_KEY")
BANK_IMAGE_BASE_URL = os.environ.get("BANK_IMAGE_BASE_URL")
API_KEY = os.environ.get("API_KEY")