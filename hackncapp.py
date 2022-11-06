# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
from datetime import datetime
from enum import Enum
import psycopg2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
from dateutil.relativedelta import relativedelta

# Create local database in the beginning
def initialize_database():
    conn = psycopg2.connect(
    host="localhost",
    database="flask_db",
    user='mmaggiore',
    password='password')
    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS person CASCADE;')

    cur.execute('CREATE TABLE person(id SERIAL PRIMARY KEY, name TEXT);')

    cur.execute('DROP TABLE IF EXISTS budget CASCADE;')
    cur.execute('CREATE TABLE budget(user_id SERIAL,budget_id SERIAL PRIMARY KEY,overall_budget_limit double precision,budget_amount double precision,FOREIGN KEY (user_id) REFERENCES person(id));')
    cur.execute('DROP TABLE IF EXISTS category CASCADE;')
    cur.execute('CREATE TABLE category(budget_id SERIAL, name TEXT PRIMARY KEY);')  #
    cur.execute('DROP TABLE IF EXISTS login CASCADE;')
    cur.execute('CREATE TABLE login(user_id SERIAL,password TEXT UNIQUE,user_name TEXT UNIQUE,FOREIGN KEY (user_id) REFERENCES person(id));')
    cur.execute('DROP TABLE IF EXISTS payment CASCADE;')
    cur.execute('CREATE TABLE payment(payment_id SERIAL PRIMARY KEY,user_id SERIAL,name TEXT,cost double precision, category_name TEXT, type_of_payment TEXT, subscription_type TEXT, due_date DATE, FOREIGN KEY (user_id) REFERENCES person(id),FOREIGN KEY (category_name) REFERENCES category(name));')
    cur.execute('DROP TABLE IF EXISTS saving_goals CASCADE;')
    cur.execute('CREATE TABLE saving_goals(user_id SERIAL,name TEXT,amount double precision,dead_line date,FOREIGN KEY (user_id) REFERENCES person(id));')
    
    conn.commit()

    cur.close()
    conn.close()
def clearEverything():
    conn = psycopg2.connect(
    host="localhost",
    database="flask_db",
    user='mmaggiore',
    password='password')
    # Open a cursor to perform database operations
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS person CASCADE;')
    cur.execute('DROP TABLE IF EXISTS budget CASCADE;')
    cur.execute('DROP TABLE IF EXISTS category CASCADE;')
    cur.execute('DROP TABLE IF EXISTS login CASCADE;')
    cur.execute('DROP TABLE IF EXISTS payment CASCADE;')
    cur.execute('DROP TABLE IF EXISTS saving_goals CASCADE;')
    
    conn.commit()

    cur.close()
    conn.close()

#CHANGE THIS!!!!!!!!!!!!!!!!!!!
CURRENT_GLOBAL_USER_ID = 1
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
budgetCategories = {
    "Entertainment":BudgetCategory("Entertainment",0,'#000000'),
    "Bills":BudgetCategory("Bills",0,'#000000')
    }

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

        stringDate = str(newSavingsGoal.deadline.year)+"-"+str(newSavingsGoal.deadline.month)+"-"+str(newSavingsGoal.deadline.day)
        # place it in side the database!!!!!!!!!!!!!
        conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user='mmaggiore',
        password='password')
        cur = conn.cursor()
        cur.execute('INSERT INTO saving_goals(name,amount,dead_line,user_id)'
        'VALUES(%s,%s,%s,%s)', (newSavingsGoal.name,newSavingsGoal.goal,date,CURRENT_GLOBAL_USER_ID))
        conn.commit()
        cur.close()
        conn.close()
        # Put database writing stuff here :)
        return index()
    return render_template('addsavingsgoal.html')

# Login page route
@app.route('/', methods=["GET","POST"])
def login():
    initialize_database()
    if request.method == 'POST':
        newLoginInfo = LoginInfo(request.form.get("username"), 
            request.form.get("password"))   
        # place it in side the database!!!!!!!!!!!!!
        conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user='mmaggiore',
        password='password')

        cur = conn.cursor()
        cur.execute('INSERT INTO person(name)'
        'VALUES(%s)',[newLoginInfo.username])
        cur.execute('INSERT INTO login(password,user_name)'
        'VALUES(%s,%s)',(newLoginInfo.password,newLoginInfo.username))
        conn.commit()
        cur.close()
        conn.close()
        
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
                # place it in side the database!!!!!!!!!!!!!

        conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user='mmaggiore',
        password='password')
        cur = conn.cursor()

        cur.execute('INSERT INTO category(name)'
        'VALUES(%s) ON CONFLICT DO NOTHING;', [formData.category])
        
        cur.execute('INSERT INTO payment(user_id, name, cost, category_name, type_of_payment, due_date)'
        'VALUES(%s, %s, %s, %s, %s, %s)',[CURRENT_GLOBAL_USER_ID, formData.name, formData.cost, formData.category,"One-time payment", formData.date])# add dollar sign in front of number? figure out later.
        
#           File "c:\Users\lunat\OneDrive\Documents\HackNC-2022\hackncapp.py", line 157, in payment_form
#           cur.execute('INSERT INTO payment(user_id,name, cost, category_name, type_of_payment)'
#           psycopg2.errors.ForeignKeyViolation: insert or update on table "payment" violates foreign key constraint "payment_category_name_fkey"
#           DETAIL:  Key (category_name)=(Entertainment) is not present in table "category".


        # cur.execute('INSERT INTO login(password,user_name)'
        # 'VALUES(%s,%s)',(newLoginInfo.password,newLoginInfo.username))
        conn.commit()
        cur.close()
        conn.close()

        budgetCategories[type].items.append(formData)
        return index()

    return render_template('addpayment.html', budgetCategories=budgetCategories)

# New Subscription Form Page Route
@app.route('/subscriptionform', methods=["GET","POST"])
def subscription_form():
    if request.method == 'POST':
        type = request.form.get('ptype')
        formData = Payment(type, 
            True,
            request.form.get('pname'),
            "{:.2f}".format(float(request.form.get('cost'))),
            request.form.get('date'),
            RenewalType[request.form.get('stype')])

        # SQL code
        conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user='mmaggiore',
        password='password')
        cur = conn.cursor()

        cur.execute('INSERT INTO category(name)'
        'VALUES(%s) ON CONFLICT DO NOTHING;', [formData.category])
        
        
        cur.execute('INSERT INTO payment(user_id, name, cost, category_name, type_of_payment, subscription_type, due_date)'
        'VALUES(%s, %s, %s, %s, %s, %s, %s)',(CURRENT_GLOBAL_USER_ID, formData.name, formData.cost, formData.category,"Recurring payment", formData.renewal_type.name, formData.date))
        conn.commit()
        cur.close()
        conn.close()
        
        budgetCategories[type].items.append(formData)
        conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user='mmaggiore',
        password='password')
        cur = conn.cursor()

        conn.commit()
        cur.close()
        conn.close()
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
    img = BytesIO()

    conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user='mmaggiore',
        password='password')
    cur = conn.cursor()

    cur.execute('SELECT due_date, sum(cost) FROM payment WHERE due_date > now() - INTERVAL \'30 days\' GROUP BY due_date ORDER BY due_date;')
    last30payment = cur.fetchall()
    
    dataMap = dict()
    for i in last30payment:
        dataMap[i[0]] = i[1]
    print(dataMap)

    x = []
    y = []

    for date,cost in dataMap.items():
        y.append(cost)
        x.append(f'{date.month}-{date.day}')

    plt.title("Daily Expenses in Last 10 Days")
    plt.xlabel('Date (Month-Day)')
    plt.ylabel('Daily Expenses (Dollars)')
    plt.xticks(fontsize=8, rotation=45)
    plt.tight_layout()
    plt.plot(x,y)   

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = [base64.b64encode(img.getvalue()).decode('utf8')]

    img2 = BytesIO()

    x = []
    y = []

    for i,date in enumerate(dataMap):
        cost = dataMap[date]
        if i == 0:
            y.append(cost)
            x.append(f'{date.month}-{date.day}')
            continue
        y.append(cost + y[i-1])
        x.append(f'{date.month}-{date.day}')

    plt.title("Cumulative Expenses in Last 30 Days")
    plt.xlabel('Date (Month-Day)')
    plt.ylabel('Total Expenses (Dollars)')
    plt.xticks(fontsize=8, rotation=45)
    plt.tight_layout()
    plt.plot(x,y)   

    plt.savefig(img2, format='png')
    plt.close()
    img2.seek(0)

    plot_url.append(base64.b64encode(img2.getvalue()).decode('utf8'))

    return render_template('categorybreakdown.html', budgetCategory=budgetCategories[name], plot_url=plot_url)

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
        for i in range(20):
            newDate = datetime.today() + relativedelta(days=i*random.randrange(1,2))
            formData = Payment(name, False, "random payment", "{:.2f}".format(random.random()*i) , newDate, RenewalType["None"])
            category.items.append(formData)

            conn = psycopg2.connect(
            host="localhost",
            database="flask_db",
            user='mmaggiore',
            password='password')
            cur = conn.cursor()

            cur.execute('INSERT INTO category(name)'
            'VALUES(%s) ON CONFLICT DO NOTHING;', [formData.category])
            
            cur.execute('INSERT INTO payment(user_id, name, cost, category_name, type_of_payment, due_date)'
            'VALUES(%s, %s, %s, %s, %s, %s)',[CURRENT_GLOBAL_USER_ID, formData.name, formData.cost, formData.category,"One-time payment", formData.date])    

            conn.commit()
        cur.close()
        conn.close()
    

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    
    app.run()
