from cs50 import SQL
from flask import Flask, redirect, request, session
from helpers import error, validate_entry

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

db = SQL("sqlite:///freelancer.db")

# Gets data from form and updates DB
def calculate_client():
    clientname = request.form.get("clientname")
    if not clientname:
        return error("Please introduce a client name.")

    hoursworked = validate_entry(request.form.get("hoursworked"))
    amountbilled = validate_entry(request.form.get("amountbilled"))
    if hoursworked == 0 or amountbilled == 0:
        return error("Please introduce hours worked and amount billed.")

    add_project_to_DB(clientname, hoursworked, amountbilled)
    return redirect("/summary")

# Checks if there is an existing entry for the client and creates/updates it
def add_project_to_DB(clientname, hoursworked, amountbilled):
    id = session["user_id"]
    DBentry = db.execute("SELECT * FROM clients WHERE user_id = ? AND client_name = ?", id, clientname)
    if len(DBentry) == 0:
        return add_client(clientname, hoursworked, amountbilled, id)
    if len(DBentry) == 1:
        return update_client(clientname, hoursworked, amountbilled, id, DBentry)
    else:
        return error("Database error.")

def add_client(clientname, hoursworked, amountbilled, id):
    rate = round((amountbilled / hoursworked), 2)
    db.execute("INSERT INTO clients (user_id, client_name, hours_worked, amount_billed, rate) VALUES(?, ?, ?, ?, ?)", id, clientname, hoursworked, amountbilled, rate)
    return

def update_client(clientname, hoursworked, amountbilled, id, DBentry):
    currenthours = DBentry[0]["hours_worked"]
    currentamount = DBentry[0]["amount_billed"]
    updatedhours = currenthours + hoursworked
    updatedamount = currentamount + amountbilled
    updatedrate = round((updatedamount / updatedhours), 2)
    db.execute("UPDATE clients SET hours_worked = ?, amount_billed = ?, rate = ? WHERE user_id = ? AND client_name = ?", updatedhours, updatedamount, updatedrate, id, clientname)
    return

def delete_client(id):
    db.execute("DELETE FROM clients WHERE id = ?", id)
    return redirect ("/summary")