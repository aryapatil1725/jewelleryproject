import pymysql
import os

def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'Aryapatil1626'),
        database=os.getenv('DB_NAME', 'jewellerydb'),
        cursorclass=pymysql.cursors.DictCursor,
        charset='utf8mb4'
    )