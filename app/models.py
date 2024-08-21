from app import db
from flask_login import UserMixin

# many to many relationship
# many accounts can have many addresses
userAddresses = db.Table('userAddresses',
    db.Column('address_id', db.Integer, db.ForeignKey('addresses.id'),
              primary_key=True),
    db.Column('account_id', db.Integer, db.ForeignKey('accounts.id'),
              primary_key=True)
)

# many accounts can have many basket items
userBasket = db.Table('userBasket',
    db.Column('basket_id', db.Integer, db.ForeignKey('basket.id'),
              primary_key=True),
    db.Column('account_id', db.Integer, db.ForeignKey('accounts.id'),
              primary_key=True)
)

# many accounts can have many orders
userOrders = db.Table('userOrders',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'),
              primary_key=True),
    db.Column('account_id', db.Integer, db.ForeignKey('accounts.id'),
              primary_key=True)
)

# many products can have many tags
productTags = db.Table('productTags',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'),
              primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'),
              primary_key=True)
)


# stores user account info
class Accounts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(500))
    lastName = db.Column(db.String(500))
    email = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(25))

    # all relationships to other tables
    address = db.relationship('Addresses', secondary=userAddresses,
                              back_populates="account", lazy='dynamic')

    accountbasket = db.relationship('Basket', secondary=userBasket,
                                    back_populates="account", lazy='dynamic')

    accountorders = db.relationship('Orders', secondary=userOrders,
                                    back_populates="account", lazy='dynamic')

    def __repr__(self):
        return '{}{}{}{}'.format(self.firstName, self.lastName, self.email,
                                 self.password)


# stores all accounts address, related to Accounts
class Addresses(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    houseNumName = db.Column(db.String(500))
    street = db.Column(db.String(500))
    town = db.Column(db.String(500))
    postcode = db.Column(db.String(7))

    # relation to Accounts
    account = db.relationship('Accounts', secondary=userAddresses,
                              back_populates="address", lazy='dynamic')

    def __repr__(self):
        return '{}{}{}{}'.format(self.houseNumName, self.street, self.town,
                                 self.postcode)


# all products, used for displaying products
class Products(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    imageName = db.Column(db.String(500))
    imageAlt = db.Column(db.String(500))
    cost = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    tags = db.relationship('Tags', secondary=productTags,
                           back_populates="product", lazy='dynamic')

    def __repr__(self):
        return '{}{}'.format(self.name, self.cost)


# the tags for the products
class Tags(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tagName = db.Column(db.String(50))

    product = db.relationship('Products', secondary=productTags,
                              back_populates="tags", lazy='dynamic')

    # returns as dict so can be used for search bar
    def as_dict(self):
        return {'tagName': self.tagName}


# user basket, related to Account
class Basket(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    productID = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    name = db.Column(db.String(500))
    cost = db.Column(db.Float)

    # relation to Account
    account = db.relationship('Accounts', secondary=userBasket,
                              back_populates="accountbasket", lazy='dynamic')

    def __repr__(self):
        return '{}{}{}{}'.format(self.productID, self.quantity, self.name,
                                 self.cost)


# orders, related to Account
class Orders(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.Integer)
    addressID = db.Column(db.Integer)
    orderDate = db.Column(db.DateTime)
    productID = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    name = db.Column(db.String(500))
    cost = db.Column(db.Float)
    totalOrderCost = db.Column(db.Float)

    # relation to Account
    account = db.relationship('Accounts', secondary=userOrders,
                              back_populates="accountorders", lazy='dynamic')

    def __repr__(self):
        return '{}{}{}{}'.format(self.orderID, self.quantity, self.name,
                                 self.cost)
