# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
from datetime import datetime

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

data = {'paymentTypes': {'type': "Entertainment",'type': "Bill",'type': "Something Else"}, 'payments': []}

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
@app.route('/', methods =["GET", "POST"])
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return render_template('paymentadditionform.html', data=data)

@app.route('/postpaymentform', methods=['POST', 'GET'])
def newPayment():
    if request.method == 'POST':
        formData = {
            'name': request.form.get('pname'),
            'amount': request.form.get('cost'), 
            'type': request.form.get('ptype')}
        
        data.payments.append(formData)
        return hello_world()

    return hello_world()

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
