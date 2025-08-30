#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Initialize Flask-RESTful API
api = Api(app)


@app.route('/')
def home():
    return '<h1>Pizza Restaurant API</h1>'


@app.route('/restaurants', methods=['GET'])
def restaurants():
    """GET /restaurants - Return all restaurants"""
    restaurants = Restaurant.query.all()
    restaurants_dict = []
    
    for restaurant in restaurants:
        restaurant_dict = restaurant.to_dict(only=('id', 'name', 'address'))
        restaurants_dict.append(restaurant_dict)
    
    return make_response(jsonify(restaurants_dict), 200)


@app.route('/restaurants/<int:id>', methods=['GET'])
def restaurant_by_id(id):
    """GET /restaurants/<int:id> - Return restaurant with restaurant_pizzas"""
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    
    if restaurant is None:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)
    
    restaurant_dict = restaurant.to_dict(only=('id', 'name', 'address', 'restaurant_pizzas'))
    
    return make_response(jsonify(restaurant_dict), 200)


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    """DELETE /restaurants/<int:id> - Delete restaurant and associated restaurant_pizzas"""
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    
    if restaurant is None:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)
    
    db.session.delete(restaurant)
    db.session.commit()
    
    return make_response('', 204)


@app.route('/pizzas', methods=['GET'])
def pizzas():
    """GET /pizzas - Return all pizzas"""
    pizzas = Pizza.query.all()
    pizzas_dict = []
    
    for pizza in pizzas:
        pizza_dict = pizza.to_dict(only=('id', 'name', 'ingredients'))
        pizzas_dict.append(pizza_dict)
    
    return make_response(jsonify(pizzas_dict), 200)


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    """POST /restaurant_pizzas - Create new RestaurantPizza"""
    data = request.get_json()
    
    try:
        # Validate that pizza and restaurant exist
        pizza = Pizza.query.filter(Pizza.id == data.get('pizza_id')).first()
        restaurant = Restaurant.query.filter(Restaurant.id == data.get('restaurant_id')).first()
        
        if not pizza or not restaurant:
            return make_response(jsonify({"errors": ["Pizza or Restaurant not found"]}), 404)
        
        # Create new RestaurantPizza
        restaurant_pizza = RestaurantPizza(
            price=data.get('price'),
            pizza_id=data.get('pizza_id'),
            restaurant_id=data.get('restaurant_id')
        )
        
        db.session.add(restaurant_pizza)
        db.session.commit()
        
        # Return the created RestaurantPizza with related data
        restaurant_pizza_dict = restaurant_pizza.to_dict(only=('id', 'price', 'pizza_id', 'restaurant_id', 'pizza', 'restaurant'))
        
        return make_response(jsonify(restaurant_pizza_dict), 201)
        
    except ValueError as e:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)
    except Exception as e:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)