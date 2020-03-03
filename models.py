from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    url = db.Column(db.Text, primary_key=True)
    price = db.Column(db.Numeric)
    last_modified = db.Column(db.DateTime)

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return 'url: {} price: {} last_modified: {}'.format(self.url, self.price, self.last_modified)


class Price(db.Model):
    url = db.Column(db.Text, primary_key=True)
    value = db.Column(db.Numeric, primary_key=True)
    last_modified = db.Column(db.DateTime)
    weight = db.Column(db.Integer)
    last_notified = db.Column(db.DateTime)

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return 'url: {} price: {} last_modified: {}'.format(self.url, self.price, self.last_modified)
