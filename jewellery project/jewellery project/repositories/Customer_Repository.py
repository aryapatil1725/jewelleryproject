from db_config import get_connection
import pymysql

class CustomerRepository:

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Customer")
        data = cursor.fetchall()
        conn.close()
        return data

    def get_by_id(self, cid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Customer WHERE CustomerID=%s", (cid,))
        data = cursor.fetchone()
        conn.close()
        return data

    def add(self, fname, lname, phone, email, address, password):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Customer (FirstName, LastName, PhoneNumber, Email, Address, Password) VALUES (%s,%s,%s,%s,%s,%s)",
            (fname, lname, phone, email, address, password)
        )
        conn.commit()
        conn.close()

    def update(self, cid, fname, lname, phone, email, address, password):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Customer SET FirstName=%s, LastName=%s, PhoneNumber=%s, Email=%s, Address=%s, Password=%s WHERE CustomerID=%s",
            (fname, lname, phone, email, address, password, cid)
        )
        conn.commit()
        conn.close()

    def delete(self, cid):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Customer WHERE CustomerID=%s", (cid,))
        conn.commit()
        conn.close()

    def customer_wise_order(self, cid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM OrderMaster WHERE CustomerID=%s",
            (cid,)
        )
        data = cursor.fetchall()
        conn.close()
        return data
