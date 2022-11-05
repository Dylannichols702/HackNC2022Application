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
    cur.execute('CREATE TABLE category(name TEXT PRIMARY KEY,budget_id SERIAL,FOREIGN KEY (budget_id) REFERENCES budget(budget_id));')
    cur.execute('DROP TABLE IF EXISTS login CASCADE;')
    cur.execute('CREATE TABLE login(user_id SERIAL,password TEXT UNIQUE,user_name TEXT UNIQUE,FOREIGN KEY (user_id) REFERENCES person(id));')
    cur.execute('DROP TABLE IF EXISTS payment CASCADE;')
    cur.execute('CREATE TABLE payment(payment_id SERIAL PRIMARY KEY,user_id SERIAL,name TEXT,cost double precision, category_name TEXT,type_of_payment TEXT,due_date DATE,FOREIGN KEY (user_id) REFERENCES person(id),FOREIGN KEY (category_name) REFERENCES category(name));')
    cur.execute('DROP TABLE IF EXISTS saving_goals CASCADE;')
    cur.execute('CREATE TABLE saving_goals(user_id SERIAL,name TEXT,amount double precision,dead_line date,FOREIGN KEY (user_id) REFERENCES person(id));')
    
    conn.commit()

    cur.close()
    conn.close()



# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

PaymentCategory = Enum("PaymentCategory",["Entertainment", "Bill", "Something Else"])
RenewalType = Enum("RenewalType",["Monthly", "Yearly", "None"])

dataset = []

# Define Savings Goal class
class SavingsGoal:
    def __init__(self, name, goal, deadline):
        self.name = name
        self.goal = goal
        self.deadline = deadline
    def parseDate(self):
        return str(self.deadline.year) + "-" + str(self.deadline.month) + "-" + str(self.deadline.day)

# Define Payment Class
class Payment:
    def __init__(self, category, issub, name, cost, date, renewal_type):
        self.category = category
        self.name = name
        self.cost = cost 
        self.date = date
        self.renewal_type = renewal_type

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/createsavingsgoal', methods =["GET", "POST"])
def create_savings_goal():
    if request.method == "POST":
        newSavingsGoal = SavingsGoal(request.form.get("goalname"),
            request.form.get("goal"), 
            datetime(int(request.form.get("year")),
            int(request.form.get("month")),
            int(request.form.get("day"))))
        # Put database writing stuff here :)
        # cur.execute('INSERT INTO saving_goals()')


        return index()
    return render_template('createsavingsgoal.html', currentyear=datetime.today().year)

# Home Page route
@app.route('/', methods =["GET", "POST"])
def index():
    return render_template('index.html', data=dataset)

# New Payment Form Page route
@app.route('/paymentform', methods=["GET","POST"])
def payment_form():
    if request.method == 'POST':
        formData = Payment(request.form.get('ptype'),
            request.form.get('pname'),
            request.form.get('cost'),
            request.form.get('date'),
            RenewalType["None"])
        
        dataset.append(formData)
        return index()

    return render_template('addpayment.html', data=PaymentCategory)

# New Subscription Form Page Route
@app.route('/subscriptionform', methods=["GET","POST"])
def subscription_form():
    if request.method == 'POST':
        formData = Payment(request.form.get('ptype'), 
            request.form.get('pname'),
            request.form.get('cost'),
            request.form.get('date'),
            request.form.get('stype'))
        
        dataset.append(formData)
        return index()

    return render_template('addsubscription.html', paymentTypes=PaymentCategory, renewalTypes=RenewalType)

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    initialize_database()
    app.run()
