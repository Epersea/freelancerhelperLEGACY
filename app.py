from cs50 import SQL
from flask import Flask, render_template, request, session
from flask_session import Session
from helpers import login_required
from usermanagement import register_user, log_user_in, log_user_out
from ratecalculator import handle_expenses, handle_hours, handle_earnings, display_rate_results
from clienttool import calculate_client, delete_client
from summary import display_summary

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///freelancer.db")

# ROUTES
# Homepage. If user is not logged in, displays page with register/login links.
# If user is logged in, tool links.
@app.route("/")
def home():
    if session.get("user_id") is None:
        return render_template("index.html")
    else:
        return render_template("loggedindex.html")

# Registration page
@app.route("/register", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("register.html")
    else:
        return register_user()

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("user_id"):
            return render_template("logged.html")
        else:
            return render_template("login.html")
    else:
        return log_user_in()

# Logout function
@app.route("/logout")
@login_required
def logout():
    return log_user_out()

# The following 4 routes form the rate calculator workflow.
# User fills a 3-page form with their details and is redirected to a results page.
# Page 1: calculate expenses
@app.route("/rate", methods=["GET", "POST"])
@login_required
def rate():
    if request.method == "GET":
        return render_template("ratecalc1.html")
    else:
        return handle_expenses()

# Page 2: calculate billable hours
@app.route("/rate2", methods=["GET", "POST"])
@login_required
def rate2():
    if request.method == "GET":
        return render_template("ratecalc2.html")
    else:
        return handle_hours()

# Page 3: calculate desired earnings
@app.route("/rate3", methods=["GET", "POST"])
@login_required
def rate3():
    if request.method == "GET":
        return render_template("ratecalc3.html")
    else:
        return handle_earnings()

# Page 4: display goal rate
@app.route("/rate4")
@login_required
def rate4():
    return display_rate_results()

# Client tools. User can introduce info about clients that is added to DB.
@app.route("/clients", methods=["GET", "POST"])
@login_required
def clients():
    if request.method == "GET":
        return render_template("clients.html")
    else:
        return calculate_client()

# Displays summary results. 4 different page designs according to info available.
@app.route("/summary")
@login_required
def summary():
    return display_summary()

# Route to handle delete client button
@app.route("/delete<id>", methods=["POST"])
@login_required
def delete(id):
    return delete_client(id)
