from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    url = db.Column(db.Text, primary_key=True)
    price = db.Column(db.Numeric)
    last_modified = db.Column(db.DateTime)
    treshold = db.Column(db.Numeric)
    auto_buy = db.Column(db.Boolean)

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return 'url: {} price: {} last_modified: {}'.format(self.url,
                                                            self.price,
                                                            self.last_modified,
                                                            self.treshold,
                                                            self.auto_buy)


class Price(db.Model):
    url = db.Column(db.Text, primary_key=True)
    value = db.Column(db.Numeric, primary_key=True)
    last_modified = db.Column(db.DateTime)
    weight = db.Column(db.Integer)
    last_notified = db.Column(db.DateTime)

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return 'url: {} price: {} last_modified: {}, weight: {}, last_notified: {}'.format(self.url,
                                                                                           self.price,
                                                                                           self.last_modified,
                                                                                           self.weight,
                                                                                           self.last_notified)


class Quantity(db.Model):
    url = db.Column(db.Text, primary_key=True)
    value = db.Column(db.Integer)
    retrieved_at = db.Column(db.DateTime, primary_key=True)

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return 'url: {} price: {} last_modified: {}'.format(self.url, self.value, self.retrieved_at)
