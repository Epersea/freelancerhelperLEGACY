from cs50 import SQL
from flask import Flask, render_template, session
from helpers import error
from operator import itemgetter

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

db = SQL("sqlite:///freelancer.db")

# Checks info available about the user and shows the corresponding template.
def display_summary():
    id = session["user_id"]
    rateinfo = check_rate_info(id)
    clientsinfo = check_clients_info(id)
    if clientsinfo == 0:
        return render_template("summary.html", rateinfo=rateinfo)
    else:
        clienttotals = get_total_clients(clientsinfo)
        goalrate = rateinfo["rate"]
        message = get_message(clientsinfo, goalrate)
        return render_template("/summary.html", rateinfo=rateinfo, message=message,
        clientsinfo = clientsinfo, totals = clienttotals)

# Checks if user has introduced info about rates. If so, returns it.
def check_rate_info(id):
    DBentry = db.execute("SELECT * FROM rates WHERE user_id = ?", id)
    if len(DBentry) > 1:
        return error("Database error.")
    if len(DBentry) == 1:
        return DBentry[0]
    else:
        return 0

# Check if user has introduced info about clients. If so, orders it by rate and returns it.
def check_clients_info(id):
    DBentry = db.execute("SELECT * FROM clients WHERE user_id = ?", id)
    if len(DBentry) == 0:
        return 0
    else:
        orderedclientsinfo = sorted(DBentry, key=itemgetter("rate"))
        return orderedclientsinfo

# Orders client info by rate and returns it.
def get_total_clients(clientsinfo):
    totals = {}
    totals["hours"] = 0
    totals["amount"] = 0
    for client in clientsinfo:
        totals["hours"] += client["hours_worked"]
        totals["amount"] += client["amount_billed"]
    totals["average"] = round((totals["amount"] / totals["hours"]), 2)
    return totals

# Checks if clients are above or below goal rate and displays message accordingly.
def get_message(clientsinfo, goalrate):
    if not goalrate:
        return ""
    message1 = "All your clients are below your goal rate. It's time for a raise!"
    message2 = "Some of your clients are below your goal rate. Maybe you need to brush up your negotiation skills a bit?"
    message3 = "All your clients are above your goal rate. Good job! Why not being a bit more ambitious?"
    lastrow = len(clientsinfo) - 1
    if clientsinfo[lastrow]["rate"] < goalrate:
        return message1
    if clientsinfo[0]["rate"] > goalrate:
        return message3
    else:
        return message2