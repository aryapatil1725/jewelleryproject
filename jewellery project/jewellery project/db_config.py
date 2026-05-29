import pymysql
import pymysql.constants

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Aryapatil1626",
        database="jewellerydb",
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4",
        ssl_disabled=True,
        auth_plugin='mysql_native_password'
    )