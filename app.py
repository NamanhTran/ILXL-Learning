from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

connection = sqlite3.connect('githubNames.db', check_same_thread=False)
db = connection.cursor()
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL, name TEXT NOT NULL, github TEXT NOT NULL)")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        form_id = request.form.get('id')
        form_name = request.form.get('name')
        form_github = request.form.get('github')
        print(form_id, form_name, form_github)
        db.execute("INSERT INTO users (id, name, github) VALUES(?, ?, ?)", (form_id, form_name, form_github))
        connection.commit()
        return "Thank you! Your input has been added."
    
    else:
        return render_template("add.html")

@app.route('/repos')
def list_names():
    db.execute("SELECT name, github FROM users")
    rows = db.fetchall()
    return render_template("repositories.html", info=rows)

@app.route('/test')
def test():
    return render_template("layout.html")

if __name__ == '__main__':
    app.run()