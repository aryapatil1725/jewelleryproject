from db_config import get_connection
import pymysql
class TypeRepository:

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM JwelleryType")
        data = cursor.fetchall()
        conn.close()
        return data

    def get_by_id(self, tid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM JwelleryType WHERE TypeId=%s", (tid,))
        data = cursor.fetchone()
        conn.close()
        return data

    def add(self, typename):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO JwelleryType (TypeName) VALUES (%s)",
            (typename,)
        )
        conn.commit()
        conn.close()

    def update(self, tid, typename):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE JwelleryType SET TypeName=%s WHERE TypeId=%s",
            (typename, tid)
        )
        conn.commit()
        conn.close()

    def delete(self, tid):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM JwelleryType WHERE TypeId=%s", (tid,))
        conn.commit()
        conn.close()

    def type_wise_product(self, typeid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Products WHERE TypeID=%s",
            (typeid,)
        )
        data = cursor.fetchall()
        conn.close()
        return data