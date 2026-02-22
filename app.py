from flask import Flask, request, render_template_string
import psycopg2

app = Flask(__name__)

DB_HOST = "gadha-postgres-server.postgres.database.azure.com"
DB_NAME = "cruddb"
DB_USER = "gadhaadmin"
DB_PASS = "X9@Secure2026!"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER + "@" + "gadha-postgres-server",
        password=DB_PASS,
        sslmode="require"
    )

@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
    """)
    cur.execute("SELECT * FROM students;")
    students = cur.fetchall()
    cur.close()
    conn.close()

    html = """
    <h2>Student CRUD App</h2>
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

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name) VALUES (%s);", (name,))
    conn.commit()
    cur.close()
    conn.close()
    return home()



