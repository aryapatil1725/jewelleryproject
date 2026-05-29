import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Aryapatil1626",
        database="jewellerydb",
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4"
    )