import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=os.getenv("DB_DSN")
    )

def run():
    print("▶ Setup database")
    conn = get_connection()
    cur = conn.cursor()

    # ===== DROP TABELLE SE ESISTONO =====
    for table in ["orders", "orders_archive"]:
        try:
            cur.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
        except:
            pass

    # ===== CREAZIONE TABELLA ORDERS =====
    cur.execute("""
        CREATE TABLE orders (
            order_id NUMBER PRIMARY KEY,
            customer_id NUMBER,
            product VARCHAR2(50),
            amount NUMBER,
            order_date DATE
        )
    """)

    # ===== CREAZIONE TABELLA ORDERS_ARCHIVE =====
    cur.execute("""
        CREATE TABLE orders_archive (
            order_id NUMBER PRIMARY KEY,
            customer_id NUMBER,
            product VARCHAR2(50),
            amount NUMBER,
            order_date DATE
        )
    """)

    # ===== INSERIMENTO DATI ORDERS =====
    cur.executemany("INSERT INTO orders VALUES (:1, :2, :3, :4, SYSDATE)", [
        (1, 1, 'Laptop', 1200),
        (2, 2, 'Mouse', 25),
        (3, 1, 'Keyboard', 45)
    ])

    # ===== INSERIMENTO DATI ORDERS_ARCHIVE =====
    cur.executemany("INSERT INTO orders_archive VALUES (:1, :2, :3, :4, SYSDATE-30)", [
        (101, 3, 'Monitor', 230),
        (102, 4, 'Printer', 180)
    ])

    conn.commit()
    print("✅ Tabelle create e dati inseriti")

    # ===== CREATE MV LOG ORDERS =====
    try:
        cur.execute("DROP MATERIALIZED VIEW LOG ON orders")
    except:
        pass

    cur.execute("""
        CREATE MATERIALIZED VIEW LOG ON orders
        WITH ROWID, PRIMARY KEY
        INCLUDING NEW VALUES
    """)
    print("✅ MV LOG su orders creato")

    # ===== CREATE MV LOG ORDERS_ARCHIVE =====
    try:
        cur.execute("DROP MATERIALIZED VIEW LOG ON orders_archive")
    except:
        pass

    cur.execute("""
        CREATE MATERIALIZED VIEW LOG ON orders_archive
        WITH ROWID, PRIMARY KEY
        INCLUDING NEW VALUES
    """)
    print("✅ MV LOG su orders_archive creato")

    cur.close()
    conn.close()

if __name__ == "__main__":
    run()
