from flask import Flask, request, render_template, redirect
import psycopg2

app = Flask(__name__)

# Database Config (Flexible Server)
DB_HOST = "gadha-postgres-server.postgres.database.azure.com"
DB_NAME = "cruddb"
DB_USER = "gadhaadmin"
DB_PASS = "Secure1234!"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        sslmode="require"
    )

# ======================
# HOME - READ
# ======================

@app.route("/")
def home():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return f"DB Connected Successfully! Result: {result}"
    except Exception as e:
        return f"Database Error: {e}"


if __name__ == "__main__":
    app.run()


