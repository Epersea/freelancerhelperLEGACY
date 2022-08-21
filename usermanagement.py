from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import error

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

db = SQL("sqlite:///freelancer.db")

# Checks if user exists and if password/confirmation are correct
# If everything goes well, user is added to DB
def register_user():
    name = request.form.get("username")
    error = ""
    if not name:
        error = "Please introduce a name."
        return render_template("register.html", error=error)

    if check_user_exists(name) == True:
        error = "This user already exists. Please try again."
        return render_template("register.html", error=error)

    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    if validate_password(password, confirmation) == False:
        error = "Introduce a password and a confirmation that match."
        return render_template("register.html", error=error)
    else:
        add_user_to_database(name, password)

    return redirect("/")

# Checks if credentials are correct, starts session and redirects to Home
def log_user_in():
    name = request.form.get("username")
    password = request.form.get("password")
    if not name:
        error = "Please introduce a name."
        return render_template("login.html", error=error)
    if not password:
        error = "Please introduce a password."
        return render_template("login.html", error=error)

    DBentry = query_user(name)
    if validate_credentials(DBentry, password) == False:
        error = "Invalid credentials. Please try again."
        return render_template("login.html", error=error)
    else:
        start_session(DBentry)

    return redirect("/")

# Clears session and redirects to Home
def log_user_out():
    session.clear()
    return redirect("/")

# Queries DB for user name and checks result length
def check_user_exists(name):
    DBentry = query_user(name)
    if len(DBentry) > 0:
        return True
    else:
        return False

# Queries database and returns user entry
def query_user(name):
    query = db.execute("SELECT * FROM users WHERE username = ?", name)
    return query

# Checks that password and confirmation are introduced and match
def validate_password(password, confirmation):
    if not password or not confirmation or password != confirmation:
        return False
    else:
        return True

# Generates password hash and adds user to users table
def add_user_to_database(username, password):
    hash = generate_password_hash(password)
    db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
    return

# Checks that user and password are correct
def validate_credentials(DBentry, password):
    if len(DBentry) != 1 or not check_password_hash(DBentry[0]["hash"], password):
        return False
    else:
        return True

# Assigns session to logged-in user
def start_session(DBentry):
    session["user_id"] = DBentry[0]["id"]
    return