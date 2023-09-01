from flask import Flask, render_template, request, redirect, url_for
import uuid


app = Flask(__name__)

data_dict = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscription', methods=['GET', 'POST'])
def subscription():
    token = None
    amount = None

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            token = str(uuid.uuid4())
            data_dict[token] = amount
            return redirect(url_for('subsuccess', token=token, amount=amount))
        except ValueError:
            return "Invalid input. Please enter a valid amount"
        
    return render_template('subscription.html', token=token)

@app.route('/subsuccess/<token>/<amount>')
def subsuccess(token, amount):
    return render_template('subsuccess.html', token=token, amount=amount)
