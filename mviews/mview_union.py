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
    print("▶ Creazione MV con UNION ALL (ON DEMAND)")
    conn = get_connection()
    cur = conn.cursor()

    # Drop MV se esiste
    try:
        cur.execute("DROP MATERIALIZED VIEW orders_mv")
    except:
        pass

    # Creazione MV ON DEMAND (default) con FAST REFRESH
    # INCLUDI IL ROWID E UN MARKER UNICO IN OGNI BLOCCO SELECT
    cur.execute("""
        CREATE MATERIALIZED VIEW orders_mv
        BUILD IMMEDIATE
        REFRESH FAST
        AS
        SELECT
            order_id,
            product,
            amount,
            1 AS source_marker,    -- Marker unico per la tabella 'orders'
            o.ROWID AS rid         -- Seleziona esplicitamente il ROWID
        FROM orders o
        UNION ALL
        SELECT
            order_id,
            product,
            amount,
            2 AS source_marker,    -- Marker unico per la tabella 'orders_archive'
            oa.ROWID AS rid        -- Seleziona esplicitamente il ROWID
        FROM orders_archive oa
    """)

    print("✅ MV creata ON DEMAND con FAST REFRESH")
    cur.close()
    conn.close()

if __name__ == "__main__":
    run()

