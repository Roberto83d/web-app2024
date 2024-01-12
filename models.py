from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # Assuming a max length of 255 characters
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    # Add more fields as needed
