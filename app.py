from flask import Flask, request, render_template, redirect
import sqlite3

# initalizes the flask server
app = Flask(__name__)

# Create the connect to our webapp and the database
connection = sqlite3.connect('githubNames.db', check_same_thread=False)
db = connection.cursor()

# Create users table if does not exist
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL, name TEXT NOT NULL, github TEXT NOT NULL)")

# Return the home page
@app.route('/')
def index():
    return render_template("index.html")

# add page route
@app.route('/add', methods=["GET", "POST"])
def form():
    # If the user hit (POST request) the submit button the add page
    if request.method == "POST":
        # Grab the data what was passed through the form
        form_id = request.form.get('id')
        form_name = request.form.get('name')
        form_github = request.form.get('github')
        
        # Insert into our database
        db.execute("INSERT INTO users (id, name, github) VALUES(?, ?, ?)", (form_id, form_name, form_github))

        # Commit the changes we have made to our tables in the database
        connection.commit()

        # Redirect the user to the repo page
        return redirect("/repos")
    
    # If GET request return the page
    else:
        return render_template("add.html")

# The repos list 
@app.route('/repos')
def list_names():
    # Select all rows from the database
    db.execute("SELECT name, github FROM users")
    rows = db.fetchall()

    # Return the repositories page with the data for jinja to parse through
    return render_template("repositories.html", info=rows)

# Run the server
if __name__ == '__main__':
    app.run()