#Here we will put our config settings (api keys, database connection, etc.)

#First we will read our .env file to get our environment variables
from dotenv import load_dotenv
load_dotenv()

import os

GOOGLE_BOOKS_KEY = os.getenv('GOOGLE_BOOKS_KEY')

GOOGLE_GENAI_KEY = os.getenv('GOOGLE_GENAI_KEY')

GOOGLE_GENAI_MODEL = os.getenv('GOOGLE_GENAI_MODEL', 'models/text-bison-001')

#Database URL for SQLAlchemy
DATABASE_URL = os.getenv('DATABASE_URL', '')

