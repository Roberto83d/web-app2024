from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=0)

class AccountBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)

class TransactionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))

# Function to create initial products
def create_initial_products():
    products = [
        {"name": "Product1", "quantity": 50},
        {"name": "Product2", "quantity": 30},
        {"name": "Product3", "quantity": 20},
        # Add more products as needed
    ]

    for prod in products:
        existing_product = Product.query.filter_by(name=prod['name']).first()
        if not existing_product:
            new_product = Product(name=prod['name'], quantity=prod['quantity'])
            db.session.add(new_product)

    db.session.commit()

# Routes
@app.route('/')
def index():
    balance = AccountBalance.query.first()
    products = Product.query.all()
    return render_template('index.html', balance=balance.balance if balance else 0, products=products)

@app.route('/zakup', methods=['POST'])
def zakup():
    try:
        product_name = request.form['produkt']
        price = float(request.form['cena'])
        quantity = int(request.form['ilosc'])
    except ValueError:
        return "Invalid input"

    product = Product.query.filter_by(name=product_name).first()
    if product:
        product.quantity += quantity  # Increase product quantity
        db.session.commit()

        transaction = TransactionHistory(description=f"Purchased {quantity} units of {product_name} at {price} per unit")
        db.session.add(transaction)
        db.session.commit()
    else:
        return "Product not found"

    return redirect(url_for('index'))

@app.route('/sprzedaz', methods=['POST'])
def sprzedaz():
    try:
        product_name = request.form['produkt']
        quantity_to_sell = int(request.form['ilosc'])
    except ValueError:
        return "Invalid input"

    product = Product.query.filter_by(name=product_name).first()
    if product and product.quantity >= quantity_to_sell:
        product.quantity -= quantity_to_sell  # Decrease product quantity
        db.session.commit()

        transaction = TransactionHistory(description=f"Sold {quantity_to_sell} units of {product_name}")
        db.session.add(transaction)
        db.session.commit()
    else:
        return "Insufficient quantity or product not found"

    return redirect(url_for('index'))

@app.route('/zmiana_stanu_konta', methods=['POST'])
def zmiana_stanu_konta():
    try:
        zmiana = float(request.form['zmiana'])
    except ValueError:
        return "Invalid input"

    balance_entry = AccountBalance.query.first()
    if balance_entry:
        balance_entry.balance += zmiana  # Update account balance
    else:
        balance_entry = AccountBalance(balance=zmiana)
        db.session.add(balance_entry)

    db.session.commit()

    transaction = TransactionHistory(description=f"Account balance changed by {zmiana}")
    db.session.add(transaction)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/historia/')
def pokaz_historie():
    historia = TransactionHistory.query.all()
    return render_template('historia.html', historia=historia)

@app.route('/historia/<int:start>/<int:koniec>')
def pokaz_fragment_historii(start, koniec):
    historia = TransactionHistory.query.slice(start, koniec).all()
    return render_template('historia.html', historia=historia)

# Main block to run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_initial_products()
    app.run(debug=True)
