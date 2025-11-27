from config.db import get_connection

def run():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE MATERIALIZED VIEW LOG ON customers
    WITH PRIMARY KEY INCLUDING NEW VALUES
    """)

    cur.execute("""
    CREATE MATERIALIZED VIEW LOG ON orders
    WITH PRIMARY KEY INCLUDING NEW VALUES
    """)

    conn.commit()
    conn.close()
    print("✅ MV LOG creati")

if __name__ == "__main__":
    run()
