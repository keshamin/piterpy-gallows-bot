import os
from ast import literal_eval


TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = literal_eval(os.getenv('ADMIN_IDS', default='[70044128]'))


# DB
DB_HOST = 'ds239578.mlab.com'
DB_PORT = 39578
DB_NAME = 'heroku_5nnl2kl4'
DB_USER = 'heroku_5nnl2kl4'
DB_PASSWORD = 'ldviu93r45k4t82517ge5d7ab3'

DB_URI = os.getenv('MONGODB_URI') or \
         f'mongodb://{DB_USER or ""}:{DB_PASSWORD or ""}@{DB_HOST or ""}:{DB_PORT or ""}/{DB_NAME or ""}'

# mLab compatibility issue
DB_URI = 'mongodb://heroku_5nnl2kl4:ldviu93r45k4t82517ge5d7ab3@ds239578.mlab.com:39578/heroku_5nnl2kl4?retryWrites=false'
