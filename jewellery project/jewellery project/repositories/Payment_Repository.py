from db_config import get_connection
import pymysql


class PaymentRepository:

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Payment")
        data = cursor.fetchall()
        conn.close()
        return data

    def get_by_id(self, pid):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Payment WHERE PaymentID=%s", (pid,))
        data = cursor.fetchone()
        conn.close()
        return data

    def add(self, oid, paymentdate, amount, method):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Payment
            (OrderID, PaymentDate, AmountPaid, PaymentMethod)
            VALUES (%s, %s, %s, %s)
            """,
            (oid, paymentdate, amount, method)
        )
        conn.commit()
        conn.close()

    def update(self, pid, oid, paymentdate, amount, method):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Payment
            SET OrderID=%s,
                PaymentDate=%s,
                AmountPaid=%s,
                PaymentMethod=%s
            WHERE PaymentID=%s
            """,
            (oid, paymentdate, amount, method, pid)
        )
        conn.commit()
        conn.close()

    def delete(self, pid):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Payment WHERE PaymentID=%s", (pid,))
        conn.commit()
        conn.close()

    def date_wise_payment(self, fdate, tdate):
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            """
            SELECT * FROM Payment
            WHERE PaymentDate BETWEEN %s AND %s
            ORDER BY PaymentDate DESC
            """,
            (fdate, tdate)
        )
        data = cursor.fetchall()
        conn.close()
        return data
