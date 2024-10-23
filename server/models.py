from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'
    
    # Relationship with Review
    reviews = db.relationship('Review', back_populates='customer')

    # Association proxy to access items through reviews
    items = association_proxy('reviews', 'item')

    # Serialization rules to prevent circular references
    serialize_rules = ('-reviews.customer',)  # Exclude reviews -> customer relationship


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
    
    # Relationship with Review
    reviews = db.relationship('Review', back_populates='item')

    # Serialization rules to prevent circular references
    serialize_rules = ('-reviews.item',)  # Exclude reviews -> item relationship

    #review model
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    
    # Foreign Keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    
    # Relationships with Customer and Item
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    # Serialization rules to prevent circular references
    serialize_rules = (
        '-customer.reviews',  # Exclude customer -> reviews relationship
        '-item.reviews',      # Exclude item -> reviews relationship
    )    
