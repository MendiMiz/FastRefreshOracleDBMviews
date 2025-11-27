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
    print("▶ Creazione MV semplice")
    conn = get_connection()
    cur = conn.cursor()

    # Drop MV se esiste
    try:
        cur.execute("DROP MATERIALIZED VIEW orders_mv")
    except:
        pass

    # Creazione MV fast refresh su alcune colonne
    cur.execute("""
        CREATE MATERIALIZED VIEW orders_mv
        BUILD IMMEDIATE
        REFRESH FAST
        AS
        SELECT order_id, product, amount
        FROM orders
    """)

    print("✅ MV semplice creata con fast refresh")
    cur.close()
    conn.close()

if __name__ == "__main__":
    run()
