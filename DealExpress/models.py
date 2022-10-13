from DealExpress import db

class Item(db.Model):
    name = db.Column(db.String(64))
    price = db.Column(db.String(64))
    id = db.Column(db.Integer, primary_key=True)
    retailer = db.Column(db.String(64))
    