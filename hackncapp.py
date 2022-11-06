# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
from datetime import datetime
from dateutil.relativedelta import relativedelta
from enum import Enum
import pandas as pd
import random

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# Define Savings Goal class
class SavingsGoal:
    def __init__(self, name, goal, deadline):
        self.name = name
        self.goal = goal
        self.deadline = deadline

# Define Payment Class
class Payment:
    def __init__(self, category, issub, name, cost, date, renewal_type):
        self.category = category
        self.issub = issub
        self.name = name
        self.cost = cost 
        self.date = date
        self.renewal_type = renewal_type

# Define Budget Category Class
class BudgetCategory:
    def __init__(self, name, budget, color):
        self.name = name
        self.budget = budget
        self.items = []
        self.color = color
        self.budgetremaining = budget
        self.budgetpercent = 100
        self.avgexpenses = 0
        self.overallbudgetpercent = 0


# Define Login Info Class
class LoginInfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Defines enum value for renewal types
RenewalType = Enum("RenewalType",["Monthly", "Yearly", "None"])

# Locally stored versions of every bill
# TODO: Query database to populate this dataset when the app is loaded.
dataset = {}

# Populate the list of budget categories
budgetCategories = {}

# Locally stored spending metrics
# TODO: Query database to populate this info when the app is open
budget = 0
currentMonthSpending = 0
currentMonthSubscriptionSpending = 0
currentMonthOneTimeSpending = 0

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/createsavingsgoal', methods =["GET", "POST"])
def create_savings_goal():
    if request.method == "POST":
        date = datetime.strptime(request.form.get("deadline"), "%Y-%m-%d")
        newSavingsGoal = SavingsGoal(request.form.get("goalname"),
            "{:.2f}".format(float(request.form.get('goal'))), 
            date)
        # Put database writing stuff here :)
        return index()
    return render_template('addsavingsgoal.html')

# Login page route
@app.route('/', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        newLoginInfo = LoginInfo(request.form.get("username"), 
            request.form.get("password"))
        generate_data()
        return render_template('index.html', user=newLoginInfo.username, data=budgetCategories)
    return render_template('login.html')

# Home Page route
@app.route('/home', methods =["GET", "POST"])
def index():
    return render_template('index.html', data=budgetCategories)

# New Payment Form Page route
@app.route('/paymentform', methods=["GET","POST"])
def payment_form():
    if request.method == 'POST':
        type = request.form.get('ptype')
        formData = Payment(type,
            False,
            request.form.get('pname'),
            "{:.2f}".format(float(request.form.get('cost'))),
            request.form.get('date'),
            RenewalType["None"])

        budgetCategories[type].items.append(formData)
        calc_budgetvalues(budgetCategories[type])
        
        return index()

    return render_template('addpayment.html', budgetCategories=budgetCategories)

# New Subscription Form Page Route
@app.route('/subscriptionform', methods=["GET","POST"])
def subscription_form():
    if request.method == 'POST':
        type = request.form.get('ptype')
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        renewalType = RenewalType[request.form.get('stype')]

        while(date < datetime.now()):
            formData = Payment(type, 
                True,
                request.form.get('pname'),
                "{:.2f}".format(float(request.form.get('cost'))),
                date,
                renewalType)

            budgetCategories[type].items.append(formData)

            if renewalType == RenewalType['Monthly']:
                date = date + relativedelta(months=1)
            elif renewalType == RenewalType['Yearly']:
                date = date + relativedelta(years=1)
            elif renewalType == RenewalType['Weekly']:
                date = date + relativedelta(weeks=1)
            else:
                break

        return index()

    return render_template('addsubscription.html', budgetCategories=budgetCategories, renewalTypes=RenewalType)

# New Budget Category Page Route
@app.route('/addbudgetcategory', methods=["GET","POST"])
def add_budget_category():
    if request.method == "POST":
        categoryName = request.form.get("catname")
        newBudgetCategory = BudgetCategory(
            categoryName,
            request.form.get("budget"),
            request.form.get("color")
        )
        if not categoryName in budgetCategories:
            budgetCategories[categoryName]=newBudgetCategory
        return index()
    return render_template('addbudgetcategory.html')

# Category Breakdown Page Route
@app.route('/categorybreakdown/<name>', methods=["GET","POST"])
def category_breakdown(name):
    # Calculate Remaining Budget
    return render_template('categorybreakdown.html', budgetCategory=budgetCategories[name])

def calc_budgetvalues(budgetCategory):
    budgetCategory.budgetremaining = budgetCategory.budget
    budgetremaining = float(budgetCategory.budgetremaining)

    # Calculate Remaining Budget
    for item in budgetCategory.items:
        budgetremaining -= float(item.cost)
    budgetCategory.budgetremaining = str("{:.2f}".format(budgetremaining))

    # Calculate Remaining Budget Percentage
    budgetpercent = (budgetremaining/float(budgetCategory.budget))*100
    budgetCategory.budgetpercent = str("{:.2f}".format(budgetpercent))

def generate_data():
    budgetCategories['Car Project'] = BudgetCategory("Car Project", "{:.2f}".format(30000.00), '#aa0000')
    budgetCategories['Italy Trip'] = BudgetCategory("Italy Trip", "{:.2f}".format(5000.00), '#0000aa')
    for name,category in budgetCategories.items():
        for i in range(100):
            newDate = datetime.now
            newData = Payment(name, False, "random payment", "{:.2f}".format(random.random()*i) , newDate, RenewalType["None"])
            category.items.append(newData)
        
        for i in range(50):
            newDate = datetime.now
            newData = Payment(name, 
                False, "random subscription", 
                "{:.2f}".format(random.random()*i), 
                newDate, 
                random.choice([RenewalType["Monthly"], RenewalType["Yearly"]]))
            category.items.append(newData)
    
        calc_budgetvalues(budgetCategories[name])

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
