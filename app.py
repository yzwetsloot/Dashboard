import json
from datetime import timedelta

from flask import Flask, request, render_template

from models import db, Product, Price, Quantity

app = Flask(__name__)

with open('config/config.json') as file:
    config = json.loads(file.read())

db_config = config['db_config']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
    **db_config)

db.init_app(app)
app.app_context().push()


@app.route('/')
def index():
    if 'search' in request.args:
        query = request.args['search']
        products, price_histories, quantity_histories = search(query)

        return render_template('index.html',
                               products=products,
                               price_histories=price_histories,
                               quantity_histories=quantity_histories)
    return render_template('index.html')


def search(query):
    query = '%{}%'.format(query)
    products = Product.query.filter(Product.url.like(query)).all()

    price_histories = {}
    quantity_histories = {}

    for product in products:
        price_history = Price.query.filter(Price.url == product.url).order_by(Price.last_modified).all()
        price_history = [(price.last_modified, price.value) for price in price_history]

        length = len(price_history)

        for i in range(1, (length - 1) * 2, 2):
            start = price_history[i - 1][0] + timedelta(seconds=1)
            price_history.insert(i, (start, price_history[i][1]))

        price_histories[product.url] = plot(*zip(*price_history), 'Price')

        quantity_history = Quantity.query.filter(Quantity.url == product.url).order_by(Quantity.retrieved_at).all()
        quantity_history = [(quantity.retrieved_at, quantity.value) for quantity in quantity_history]

        if quantity_history:
            quantity_histories[product.url] = plot(*zip(*quantity_history), 'Quantity')
        else:
            quantity_histories[product.url] = '{"data":[], "layout": {"title":"Quantity"}}'

    return products, price_histories, quantity_histories


def plot(x, y, title):
    x = json.dumps([str(item) for item in x])
    y = json.dumps([float(item) for item in y])
    figure = f'{{"data": [{{"x": {x}, "y": {y}, "line": {{"color": "#636EFA"}}}}],' + \
             f'"layout": {{"title": "{title}", "xaxis": {{"type": "date"}}, "yaxis": {{"type": "linear",' \
             '"rangemode": "tozero", "autorange": "true"}}}'
    return figure


if __name__ == '__main__':
    app.run(debug=True)
