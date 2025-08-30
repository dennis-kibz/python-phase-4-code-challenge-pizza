#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

fake = Faker()

with app.app_context():

    # Clear existing data
    RestaurantPizza.query.delete()
    Restaurant.query.delete()
    Pizza.query.delete()
    
    # Create restaurants
    restaurants = []
    restaurants.append(Restaurant(name="Karen's Pizza Shack", address="address1"))
    restaurants.append(Restaurant(name="Sanjay's Pizza", address="address2"))
    restaurants.append(Restaurant(name="Kiki's Pizza", address="address3"))
    
    db.session.add_all(restaurants)
    
    # Create pizzas
    pizzas = []
    pizzas.append(Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese"))
    pizzas.append(Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni"))
    pizzas.append(Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard"))
    pizzas.append(Pizza(name="Margherita", ingredients="Dough, Tomato Sauce, Mozzarella, Basil"))
    pizzas.append(Pizza(name="Hawaiian", ingredients="Dough, Tomato Sauce, Cheese, Ham, Pineapple"))
    
    db.session.add_all(pizzas)
    
    # Commit restaurants and pizzas first to get their IDs
    db.session.commit()
    
    # Create restaurant pizzas
    restaurant_pizzas = []
    
    # Ensure each restaurant has at least one pizza
    for i, restaurant in enumerate(restaurants):
        pizza = pizzas[i % len(pizzas)]
        rp = RestaurantPizza(
            price=randint(1, 30),
            restaurant_id=restaurant.id,
            pizza_id=pizza.id
        )
        restaurant_pizzas.append(rp)
    
    # Add some random additional relationships
    for _ in range(7):  # Add 7 more random restaurant-pizza relationships
        restaurant = rc(restaurants)
        pizza = rc(pizzas)
        # Check if this combination already exists
        existing = RestaurantPizza.query.filter_by(
            restaurant_id=restaurant.id, 
            pizza_id=pizza.id
        ).first()
        
        if not existing:
            rp = RestaurantPizza(
                price=randint(1, 30),
                restaurant_id=restaurant.id,
                pizza_id=pizza.id
            )
            restaurant_pizzas.append(rp)
    
    db.session.add_all(restaurant_pizzas)
    db.session.commit()
    
    print("🍕 Seeded database with restaurants, pizzas, and restaurant_pizzas!")
    print(f"Created {len(restaurants)} restaurants")
    print(f"Created {len(pizzas)} pizzas") 
    print(f"Created {len(restaurant_pizzas)} restaurant_pizzas")