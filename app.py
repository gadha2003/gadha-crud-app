from flask import Flask, request, render_template_string
import psycopg2
import os

app = Flask(__name__)

# ==========================
# Azure PostgreSQL Settings
# ==========================

DB_HOST = "gadha-postgres-server.postgres.database.azure.com"
DB_NAME = "cruddb"
DB_USER = "gadhaadmin@gadha-postgres-server"
DB_PASS = "X9@Secure2026!"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        sslmode="require"
    )

# ==========================
# Home Route
# ==========================

@app.route("/")
def home():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100)
            );
        """)
        conn.commit()

        cur.execute("SELECT * FROM students;")
        students = cur.fetchall()

        cur.close()
        conn.close()

    except Exception as e:
        return f"<h3>Database Error:</h3><pre>{e}</pre>"

    html = """
    <h2>Student CRUD App (Azure PostgreSQL)</h2>

    <form method="POST" action="/add">
        <input type="text" name="name" placeholder="Enter name" required>
        <button type="submit">Add</button>
    </form>

    <ul>
    {% for student in students %}
        <li>{{student[1]}}</li>
    {% endfor %}
    </ul>
    """

    return render_template_string(html, students=students)

# ==========================
# Add Route
# ==========================

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO students (name) VALUES (%s);", (name,))
        conn.commit()

        cur.close()
        conn.close()

    except Exception as e:
        return f"<h3>Insert Error:</h3><pre>{e}</pre>"

    return home()

# ==========================
# Main
# ==========================

if __name__ == "__main__":
    app.run()
