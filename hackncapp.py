# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
from datetime import datetime
from enum import Enum

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

PaymentCategory = Enum("PaymentCategory",["Entertainment", "Bill", "Something Else"])
RenewalType = Enum("RenewalType",["Monthly", "Yearly", "None"])

dataset = {}

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
        self.issub = issub
        self.name = name
        self.cost = cost 
        self.date = date
        self.renewal_type = renewal_type

class LoginInfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password

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
    return render_template('addsavingsgoal.html', currentyear=datetime.today().year)

@app.route('/', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        newLoginInfo = LoginInfo(request.form.get("username"), 
            request.form.get("password"))
        return index()
    return render_template('login.html')

# Home Page route
@app.route('/home', methods =["GET", "POST"])
def index():
    return render_template('index.html', data=dataset)

# New Payment Form Page route
@app.route('/paymentform', methods=["GET","POST"])
def payment_form():
    if request.method == 'POST':
        formData = Payment(request.form.get('ptype'),
            False,
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
            True,
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
    app.run()
