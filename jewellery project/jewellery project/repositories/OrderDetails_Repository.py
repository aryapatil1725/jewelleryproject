from db_config import get_connection
import pymysql


class OrderDetailsRepository:

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
            SELECT 
                od.OrderDetailID,
                od.OrderID,
                od.ProductID,
                p.ProductName,
                od.Quantity,
                od.Rate,
                od.Subtotal
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
        """)

        data = cursor.fetchall()
        conn.close()
        return data

    def get_by_id(self, id):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM OrderDetails WHERE OrderDetailID=%s", (id,))
        data = cursor.fetchone()
        conn.close()
        return data

    def add(self, oid, pid, qty, rate, subtotal):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO OrderDetails
            (OrderID, ProductID, Quantity, Rate, Subtotal)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (oid, pid, qty, rate, subtotal)
        )
        conn.commit()
        conn.close()

    def update(self, id, oid, pid, qty, rate, subtotal):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE OrderDetails
            SET OrderID=%s,
                ProductID=%s,
                Quantity=%s,
                Rate=%s,
                Subtotal=%s
            WHERE OrderDetailID=%s
            """,
            (oid, pid, qty, rate, subtotal, id)
        )
        conn.commit()
        conn.close()

    def delete(self, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM OrderDetails WHERE OrderDetailID=%s", (id,))
        conn.commit()
        conn.close()

    def get_by_product(self, pid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT 
                od.OrderDetailID,
                od.OrderID,
                od.ProductID,
                p.ProductName,
                od.Quantity,
                od.Rate,
                od.Subtotal,
                om.OrderDate
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            JOIN OrderMaster om ON od.OrderID = om.OrderID
            WHERE od.ProductID=%s
            ORDER BY om.OrderDate DESC
            """,
            (pid,)
        )
        data = cursor.fetchall()
        conn.close()
        return data

    def get_sales_by_product(self, pid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT 
                od.ProductID,
                p.ProductName,
                SUM(od.Quantity) as TotalQuantity,
                SUM(od.Subtotal) as TotalSales,
                COUNT(od.OrderID) as TotalOrders
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            WHERE od.ProductID=%s
            GROUP BY od.ProductID, p.ProductName
            """,
            (pid,)
        )
        data = cursor.fetchall()
        conn.close()
        return data
