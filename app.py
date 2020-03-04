import json

from flask import Flask, request, render_template

from models import db, Product, Price

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
        products = search(query)
        return render_template('index.html', products=products)
    return render_template('index.html')


def search(query):
    query = '%{}%'.format(query)
    records = Product.query.filter(Product.url.like(query)).all()
    return records


if __name__ == '__main__':
    app.run(debug=True)
