from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)

    def __init__(self, name, price):
        self.name = name
        self.price = price

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    all_products = Product.query.all()
    products_data = []
    for product in all_products:
        product_data = {'id': product.id, 'name': product.name, 'price': product.price}
        products_data.append(product_data)
    return jsonify({'data': products_data})

@app.route('/products/update', methods=['PUT'])
def update_product():
    product_id = request.form['id']
    name = request.form['name']
    price = request.form['price']

    product = Product.query.get(product_id)
    if product:
        product.name = name
        product.price = price
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})
    else:
        return jsonify({'message': 'Product not found'})

@app.route('/products/delete', methods=['DELETE'])
def delete_product():
    product_id = request.form['id']

    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    else:
        return jsonify({'message': 'Product not found'})

@app.route('/products/add', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']

    new_product = Product(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
