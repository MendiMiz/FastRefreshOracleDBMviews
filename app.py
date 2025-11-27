from flask import Flask, render_template, request, redirect, url_for, jsonify
# Assumi che 'get_connection' sia definito qui
from config.db import get_connection
import time
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # Inizializza la connessione all'inizio della funzione
    conn = get_connection()
    cur = conn.cursor()

    # --- Handling Inserts ---
    if request.method == "POST" and "insert_orders" in request.form:
        try:
            cur.execute(
                "INSERT INTO orders (order_id, customer_id, product, amount, order_date) "
                "VALUES (:1, :2, :3, :4, SYSDATE)",
                (request.form["order_id"], request.form["customer_id"], request.form["product"], request.form["amount"])
            )
            conn.commit()
        except Exception as e:
            print(f"Error inserting into orders: {e}")
            conn.rollback()

    elif request.method == "POST" and "insert_archive" in request.form:
        try:
            cur.execute(
                "INSERT INTO orders_archive (order_id, customer_id, product, amount, order_date) "
                "VALUES (:1, :2, :3, :4, SYSDATE)",
                (request.form["archive_order_id"], request.form["archive_customer_id"], request.form["archive_product"],
                 request.form["archive_amount"])
            )
            conn.commit()
        except Exception as e:
            print(f"Error inserting into orders_archive: {e}")
            conn.rollback()

    # --- Reading Data ---
    cur.execute("SELECT * FROM orders ORDER BY order_id")
    orders = cur.fetchall()

    cur.execute("SELECT * FROM orders_archive ORDER BY order_id")
    orders_archive = cur.fetchall()

    # Seleziona le colonne corrette per l'MV, inclusi i marker (RID non serve nel frontend)
    cur.execute("SELECT order_id, product, amount, source_marker FROM orders_mv ORDER BY order_id")
    mview = cur.fetchall()

    cur.close()
    conn.close()

    # Passa i dati al template HTML
    return render_template("index.html", orders=orders, orders_archive=orders_archive, mview=mview)


@app.route("/refresh_mv", methods=["POST"])
def refresh_mv():
    """
    Endpoint API per gestire il refresh asincrono della MV e misurare il tempo.
    """
    conn = get_connection()
    cur = conn.cursor()
    # Prende il metodo da JS, di default 'F' (FAST)
    method = request.json.get('method', 'F')

    start_time = time.time()
    try:
        if method == 'C':
            print("Eseguo COMPLETE Refresh...")
            cur.execute("BEGIN DBMS_MVIEW.REFRESH('ORDERS_MV', method => 'C'); END;")
        else:
            print("Eseguo FAST Refresh...")
            cur.execute("BEGIN DBMS_MVIEW.REFRESH('ORDERS_MV', method => 'F'); END;")
        conn.commit()
        end_time = time.time()
        # Tempo in secondi, arrotondato a 3 decimali
        duration = round(end_time - start_time, 3)

        cur.close()
        conn.close()
        # Restituisce il tempo e un messaggio in formato JSON
        return jsonify({'status': 'success', 'duration': duration, 'method': method})

    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        print(f"Errore durante il refresh: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == "__main__":
    # Assicurati di aver eseguito prima lo script di setup tabelle e MV LOGS
    app.run(debug=True)
