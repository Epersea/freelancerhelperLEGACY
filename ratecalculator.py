from cs50 import SQL
from flask import Flask, render_template, redirect, request, session
from helpers import error, validate_entry

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

db = SQL("sqlite:///freelancer.db")

# Calculates total annual expenses and adds to DB
def handle_expenses():
    annual_expenses = calculate_expenses()
    add_expenses_to_DB(annual_expenses)
    return redirect("/rate2")

# Gets hours from form, calculates billable % and hours/year and adds into DB
def handle_hours():
    hoursperday = validate_entry(request.form.get("hoursperday"))
    billablepercent = calculate_billable_percent()
    billablehoursperyear = calculate_billable_hours()
    add_hours_to_DB(hoursperday, billablepercent,billablehoursperyear)
    return redirect("/rate3")

# Gets inputs from form, calculates gross year and goal rate, adds info to DB
def handle_earnings():
    netmonth = validate_entry(request.form.get("netmonth"))
    taxpercent = validate_entry(request.form.get("taxpercent"))
    id = session["user_id"]
    DBentry = get_data_from_DB(id)
    grossyear = calculate_gross_year(netmonth, taxpercent, DBentry)
    goalrate = calculate_goal_rate(grossyear, DBentry)
    add_earnings_to_DB(goalrate, netmonth, taxpercent, grossyear, id)
    return redirect("/rate4")

# Gets info from DB and renders template with variables
def display_rate_results():
    id = session["user_id"]
    rateinfo = get_data_from_DB(id)
    return render_template("ratecalc4.html", rateinfo = rateinfo)

# Gets fixed, yearly and monthly expenses and adds them up
def calculate_expenses():
    fixed = calculate_fixed_expenses()
    yearly = validate_entry(request.form.get("yearly"))
    monthly = calculate_monthly_expenses()
    annual_expenses = round((fixed + yearly + monthly), 2)
    return annual_expenses

# Gets amount and years of amortization from form, calculates expense and adds all them.
def calculate_fixed_expenses():
    fixed1amount = validate_entry(request.form.get("fixed1amount"))
    fixed1years = validate_entry(request.form.get("fixed1years"))
    fixed1 = get_fixed_expense(fixed1amount, fixed1years)
    fixed2amount = validate_entry(request.form.get("fixed2amount"))
    fixed2years = validate_entry(request.form.get("fixed2years"))
    fixed2 = get_fixed_expense(fixed2amount, fixed2years)
    fixed3amount = validate_entry(request.form.get("fixed3amount"))
    fixed3years = validate_entry(request.form.get("fixed3years"))
    fixed3 = get_fixed_expense(fixed3amount, fixed3years)
    fixed4amount = validate_entry(request.form.get("fixed4amount"))
    fixed4years = validate_entry(request.form.get("fixed4years"))
    fixed4 = get_fixed_expense(fixed4amount, fixed4years)
    total_fixed = fixed1 + fixed2 + fixed3 + fixed4
    return total_fixed

# Gets monthly amount from form and multiplies to get yearly amount.
def calculate_monthly_expenses():
    amount = validate_entry(request.form.get("monthly"))
    monthly_per_year = amount * 12
    return monthly_per_year

# Validates amounts and calculates total expense
def get_fixed_expense(amount, years):
    if amount == 0 or years == 0:
        fixed_expense = 0
    else:
        fixed_expense = amount / years
    return fixed_expense

# Checks if user already has rate info and creates/updates DB consequently
def add_expenses_to_DB(annual_expenses):
    id = session["user_id"] # Function that returns object or 2 functions
    DBentry = db.execute("SELECT * FROM rates WHERE user_id = ?", id)
    if len(DBentry) == 0:
        db.execute("INSERT INTO rates (user_id, annual_expenses) VALUES(?, ?)", id, annual_expenses)
    elif len(DBentry) == 1:
        db.execute("UPDATE rates SET annual_expenses = ? WHERE user_id = ?", annual_expenses, id)
    else:
        return error("Database error.")

# Gets billable hours per day and working days and calculates billable hours/year
def calculate_billable_hours():
    billablehoursperday = calculate_hours_per_day()
    workingdays = calculate_working_days()
    billablehoursperyear = workingdays * billablehoursperday
    return billablehoursperyear

# Gets hours per day and billable percent and calculates number of billable hours per day
def calculate_hours_per_day():
    hoursperday = validate_entry(request.form.get("hoursperday"))
    billablepercent = calculate_billable_percent()
    billablehoursperday = hoursperday * billablepercent / 100
    return billablehoursperday

# Gets working days per week and non working days per year and calculates working days.
def calculate_working_days():
    daysperweek = validate_entry(request.form.get("daysperweek"))
    holidays = validate_entry(request.form.get("holidays"))
    trainingdays = validate_entry(request.form.get("trainingdays"))
    sickdays = validate_entry(request.form.get("sickdays"))
    nonworkingdays = holidays + trainingdays + sickdays
    workingdays = daysperweek * 52 - nonworkingdays
    return workingdays

# Gets non-billable percent and calculates billable percent
def calculate_billable_percent():
    nonbillablepercent = validate_entry(request.form.get("percentnonbillable"))
    billablepercent = 100 - nonbillablepercent
    return billablepercent

# Adds hours/day, billable percent and hours/year to relevant DB entry
def add_hours_to_DB(hoursperday, billablepercent,billablehoursperyear):
    id = session["user_id"]
    get_data_from_DB(id)
    db.execute("UPDATE rates SET hours_day = ?, billable_percent = ?, billable_hours_year = ? WHERE user_id = ?", hoursperday, billablepercent, billablehoursperyear, id)
    return

# Calculates gross/year taking into account net month, tax percent and expenses
def calculate_gross_year(netmonth, taxpercent, DBentry):
    expenses = DBentry["annual_expenses"]
    grossyear = round((netmonth * 12 * ((100 + taxpercent) / 100) + expenses), 2)
    return grossyear

# Gets hours/year and calculates goal rate
def calculate_goal_rate(grossyear, DBentry):
    billablehoursperyear = DBentry["billable_hours_year"]
    goalrate = round((grossyear / billablehoursperyear), 2)
    return goalrate

# Adds goal rate, net month, tax percent and gross/year to relevant DB entry
def add_earnings_to_DB(goalrate, netmonth, taxpercent, grossyear, id):
    get_data_from_DB(id)
    db.execute("UPDATE rates SET rate = ?, net_month = ?, tax_percent = ?, gross_year = ? WHERE user_id = ?", goalrate, netmonth, taxpercent, grossyear, id)
    return

# Gets the relevant DB entry and handles unexpected results
def get_data_from_DB(id):
    DBentry = db.execute("SELECT * FROM rates WHERE user_id = ?", id)
    if len(DBentry) != 1:
        return error("Database error.")
    else:
        return DBentry[0]