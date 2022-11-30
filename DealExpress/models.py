from DealExpress import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Item(db.Model):
    name = db.Column(db.String(64))
    price = db.Column(db.String(64))
    id = db.Column(db.Integer, primary_key=True)
    item_image = db.Column(db.String(64))
    retailer = db.Column(db.String(64))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    