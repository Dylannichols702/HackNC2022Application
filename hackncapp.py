# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
from datetime import datetime

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

dataset = {'payment_types': ["Entertainment", "Bill", "Something Else"], 'payments': []}

# Define Savings Goal class
class SavingsGoal:
    def __init__(self, name, goal, deadline):
        self.name = name
        self.goal = goal
        self.deadline = deadline

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/createsavingsgoal', methods =["GET", "POST"])
def create_savings_goal():
    if request.method == "POST":
        newSavingsGoal = SavingsGoal(request.form.get("goalname"), request.form.get("goal"), datetime.today())
        return newSavingsGoal.name + " " + newSavingsGoal.goal
        
    return render_template('createsavingsgoal.html')

@app.route('/', methods =["GET", "POST"])
# ‘/’ URL is bound with hello_world() function.
def index():
    return render_template('index.html', data=dataset)

@app.route('/paymentform', methods=["GET","POST"])
def payment_form():
    return render_template('paymentadditionform.html', data=dataset['payment_types'])

@app.route('/postpaymentform', methods=['POST', 'GET'])
def newPayment():
    if request.method == 'POST':
        formData = {
            'name': request.form.get('pname'),
            'amount': request.form.get('cost'), 
            'type': request.form.get('ptype')}
        
        dataset['payments'].append(formData)
        return index()

    return index()

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
