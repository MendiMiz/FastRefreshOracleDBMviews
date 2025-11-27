from config.db import get_connection

def refresh_all():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("BEGIN DBMS_MVIEW.REFRESH('ORDERS_MV','FAST'); END;")
    cur.execute("BEGIN DBMS_MVIEW.REFRESH('SALES_MV_AGG','FAST'); END;")

    conn.commit()
    conn.close()
    print("🔄 Refresh completato")

if __name__ == "__main__":
    refresh_all()
