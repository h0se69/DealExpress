from DealExpress import db

class Item(db.Model):
    name = db.Column(db.String(64))
    price = db.Column(db.String(64))
    id = db.Column(db.Integer, primary_key=True)
    retailer = db.Column(db.String(64))
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    password1 = db.Column(db.String(128))
    
