# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
from datetime import datetime
from enum import Enum
import psycopg2

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

#CHANGE THIS!!!!!!!!!!!!!!!!!!!
CURRENT_GLOBAL_USER_ID = 1

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
    def __init__(self, name, budget, items, color):
        self.name = name
        self.budget = budget
        self.items = items
        self.color = color

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
    "Entertainment":BudgetCategory("Entertainment",0,[],'#000000'),
    "Bills":BudgetCategory("Bills",0,[],'#000000')
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
            request.form.get("goal"), 
            datetime(int(request.form.get("year")),
            int(request.form.get("month")),
            int(request.form.get("day"))))

        stringDate = str(newSavingsGoal.deadline.year)+"-"+str(newSavingsGoal.deadline.month)+"-"+str(newSavingsGoal.deadline.day)
        # place it in side the database!!!!!!!!!!!!!
        conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user='mmaggiore',
        password='password')
        cur = conn.cursor()
        cur.execute('INSERT INTO saving_goals(name,amount,dead_line,user_id)'
        'VALUES(%s,%s,%s,%s)', (newSavingsGoal.name,newSavingsGoal.goal,stringDate,CURRENT_GLOBAL_USER_ID))
        conn.commit()
        cur.close()
        conn.close()

        # Put database writing stuff here :)
        return index()
    return render_template('addsavingsgoal.html')

# Login page route
@app.route('/', methods=["GET","POST"])
def login():
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
        
        return index()
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
            request.form.get('cost'),
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
        'VALUES(%s);', [formData.category])
        
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
            request.form.get('cost'),
            request.form.get('date'),
            request.form.get('stype'))

        # SQL code
        conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user='mmaggiore',
        password='password')
        cur = conn.cursor()

        cur.execute('INSERT INTO category(name)'
        'VALUES(%s)',(formData.name))
        
        cur.execute('INSERT INTO payment(user_id, name, cost, category_name, type_of_payment, subscription_type, due_date)'
        'VALUES(%s, %s, %s, %s, %s, %s, %s)',(CURRENT_GLOBAL_USER_ID, formData.name, formData.cost, formData.category,"Recurring payment", formData.renewal_type, formData.date))
        # cur.execute('INSERT INTO login(password,user_name)'
        # 'VALUES(%s,%s)',(newLoginInfo.password,newLoginInfo.username))
        conn.commit()
        cur.close()
        conn.close()
        
        budgetCategories[type].items.append(formData)
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
            {},
            request.form.get("color")
        )
        if not categoryName in budgetCategories:
            budgetCategories[categoryName]=newBudgetCategory
        return index()
    return render_template('addbudgetcategory.html')

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    initialize_database()
    app.run()
