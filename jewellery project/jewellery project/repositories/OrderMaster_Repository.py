from db_config import get_connection
import pymysql


class OrderMasterRepository:

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
        SELECT 
            OrderMaster.OrderID,
            OrderMaster.CustomerID,
            Customer.FirstName,
            OrderMaster.OrderDate,
            OrderMaster.TotalAmount,
            OrderMaster.GSTAmt,
            OrderMaster.GrandTotal
        FROM OrderMaster
        JOIN Customer
        ON OrderMaster.CustomerID = Customer.CustomerID
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    def get_by_id(self, oid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM OrderMaster WHERE OrderID=%s", (oid,))
        data = cursor.fetchone()
        conn.close()
        return data

    def add(self, cid, orderdate, total, labour, gst, grand):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO OrderMaster
            (CustomerID, OrderDate, TotalAmount, LabourCharges, GSTAmt, GrandTotal)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (cid, orderdate, total, labour, gst, grand)
        )
        conn.commit()
        conn.close()


    def update(self, oid, cid, orderdate, total, labour, gst, grand):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE OrderMaster
            SET CustomerID=%s,
                OrderDate=%s,
                TotalAmount=%s,
                LabourCharges=%s,
                GSTAmt=%s,
                GrandTotal=%s
            WHERE OrderID=%s
            """,
            (cid, orderdate, total, labour, gst, grand, oid)
        )
        conn.commit()
        conn.close()

    def delete(self, oid):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM OrderMaster WHERE OrderID=%s", (oid,))
        conn.commit()
        conn.close()

    def get_by_customer(self, cid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT 
                OrderID,
                OrderDate,
                TotalAmount,
                LabourCharges,
                GSTAmt,
                GrandTotal
            FROM OrderMaster
            WHERE CustomerID = %s
        """, (cid,))

        data = cursor.fetchall()
        conn.close()
        return data

    def date_wise_order(self, fdate, tdate):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT OrderID, CustomerID, OrderDate, TotalAmount, GrandTotal
            FROM OrderMaster
            WHERE OrderDate BETWEEN %s AND %s
        """, (fdate, tdate))

        data = cursor.fetchall()
        conn.close()
        return data