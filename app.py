from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Gadha! Your Azure App is Running 🚀"

if __name__ == "__main__":
    app.run()