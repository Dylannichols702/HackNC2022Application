# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
from datetime import datetime

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

data = [{'type': "Entertainment"},{'type': "Bill"},{'type': "Something Else"}]

# Define Savings Goal class
class SavingsGoal:
    def __init__(self, name, goal, deadline):
        self.name = name
        self.goal = goal
        self.deadline = deadline
    def parseDate(self):
        return str(self.deadline.year) + "-" + str(self.deadline.month) + "-" + str(self.deadline.day)

# Define Subscription Class
class Subscription:
    def __init__(self, name, cost, renewaldate):
        self.name = name
        self.cost = cost
        self.renewaldate = renewaldate

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
            request.form.get("goal"), datetime(2022,5,14))
        return newSavingsGoal.name + " " + newSavingsGoal.goal + " " + SavingsGoal.parseDate(newSavingsGoal)
        
    return render_template('createsavingsgoal.html')

# Home Page
@app.route('/', methods =["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/paymentform', methods=["GET","POST"])
def payment_form():
    return render_template('paymentadditionform.html', data=data)

@app.route('/postform', methods=['POST', 'GET'])
def acceptFormData():
    if request.method == 'POST':
        formData = {
            'name': request.form.get('pname'),
            'amount': request.form.get('cost'), 
            'type': request.form.get('ptype')}
        
        print(request)
        return render_template('postformtest.html', data=formData)

    return render_template('index.html', data=data)

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
