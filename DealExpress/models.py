from DealExpress import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.String(64))
    #item_image = db.Column()
    retailer = db.Column(db.String(64))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlist.id'))
    
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    activate = db.Column(db.Integer)
    wishlist = db.relationship('Wishlist', backref = 'User')

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    #create relationship with item table, one category to many items
    items = db.relationship('Item', backref='Category')

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='Wishlist')
    