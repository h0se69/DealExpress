from DealExpress import db
from flask_login import UserMixin
    
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    active = db.Column(db.Integer)
    _wishlist = db.relationship("Wishlist", uselist=False, backref='user')

class Wishlist(db.Model): #should be one to one, each user has one wishlist consisting of collection of items
    __tablename__ = 'wishlists'
    id = db.Column(db.Integer, primary_key=True)
    
    parent_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #users = db.relationship("User", back_populates="_wishlist")

    _item = db.relationship("Item", backref='wishlist')
    #item_id = db.Column(db.Integer)#will be used to fetch item from Item table
    def __repr__(self):
        return f'<{self.id}>'

    
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64))
    price = db.Column(db.String(64))
    link = db.Column(db.String(512))

    parent_id = db.Column(db.Integer, db.ForeignKey("wishlists.id"))