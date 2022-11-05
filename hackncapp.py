# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
from datetime import datetime
from enum import Enum

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

PaymentCategory = Enum("PaymentCategory",["Entertainment", "Bill", "Something Else"])

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
    def __init__(self, category, issub, name, cost):
        self.category = category
        self.issub = issub
        self.name = name
        self.cost = cost 

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
            request.form.getlist('sub'), 
            request.form.get('pname'),
            request.form.get('cost'))
        
        dataset.append(formData)
        return index()

    return render_template('paymentadditionform.html', data=PaymentCategory)

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
