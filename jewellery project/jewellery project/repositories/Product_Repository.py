from db_config import get_connection
import pymysql
class ProductRepository:

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT 
                p.ProductID,
                p.ProductName,
                t.TypeName,
                p.ForGender,
                p.Weight,
                p.QuantityInStock
            FROM Products p
            JOIN JwelleryType t ON p.TypeID = t.TypeID order by p.ProductID
        """)

        data = cursor.fetchall()
        conn.close()
        return data

    def get_by_id(self, pid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Products WHERE ProductID=%s", (pid,))
        data = cursor.fetchone()
        conn.close()
        return data

    def add(self, pname, typeid, gender, weight, qty, desc, photo):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO Products 
               (ProductName, TypeID, ForGender, Weight, QuantityInStock, Description, Photo)
               VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (pname, typeid, gender, weight, qty, desc, photo)
        )
        conn.commit()
        conn.close()

    def product_wise_sales(self, pid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM OrderDetails WHERE ProductID=%s",
            (pid,)
        )
        data = cursor.fetchall()
        conn.close()
        return data

    def update(self, pid, pname, typeid, gender, weight, qty, desc, photo):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE Products SET 
               ProductName=%s, TypeID=%s, ForGender=%s, Weight=%s,
               QuantityInStock=%s, Description=%s, Photo=%s
               WHERE ProductID=%s""",
            (pname, typeid, gender, weight, qty, desc, photo, pid)
        )
        conn.commit()
        conn.close()

    def delete(self, pid):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Products WHERE ProductID=%s", (pid,))
        conn.commit()
        conn.close()

    def get_by_type(self, typeid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM Products WHERE TypeID=%s", (typeid,))
        data = cursor.fetchall()

        conn.close()
        return data

