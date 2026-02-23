from flask import Flask, request, render_template, redirect
import psycopg2

app = Flask(__name__)

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
        sslmode="require",
        connect_timeout=5
    )

# ======================
# HOME (READ)
# ======================

@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students ORDER BY id;")
    students = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", students=students)

# ======================
# CREATE
# ======================

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO students (name) VALUES (%s);", (name,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")

# ======================
# DELETE
# ======================

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id = %s;", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")

# ======================
# EDIT
# ======================

@app.route("/edit/<int:id>")
def edit(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE id = %s;", (id,))
    student = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("edit.html", student=student)

# ======================
# UPDATE
# ======================

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    name = request.form["name"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE students SET name = %s WHERE id = %s;", (name, id))
    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run()
