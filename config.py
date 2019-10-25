import os
from ast import literal_eval


TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = literal_eval(os.getenv('ADMIN_IDS'))


# DB
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

DB_URI = os.getenv('MONGODB_URI') or \
         f'mongodb://{DB_USER or ""}:{DB_PASSWORD or ""}@{DB_HOST or ""}:{DB_PORT or ""}/{DB_NAME or ""}'
