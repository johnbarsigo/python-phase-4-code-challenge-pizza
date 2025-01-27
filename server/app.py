#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


class Restaurant ( Resource ) :
    def get_restaurant ( self ) :
        restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
        return make_response( jsonify(restaurants), 200 )

api.add_resource(Restaurant, '/restaurants', endpoint='restaurants')

class RestaurantById ( Resource ) :
    def restaurant_by_id ( self, id ) :
        restaurant_match = [ Restaurant.query.filter_by(id=id).first().to_dict() ]

        if restaurant_match :
            return make_response( jsonify(restaurant_match), 200 )
        else :
            return make_response ( {"error": "Restaurant not found"}, 404 )
    
    def delete_by_id ( self, id ) :
        restaurant_match = Restaurant.query.filter_by(id=id).first()
        if restaurant_match :
            db.session.delete(restaurant_match)
            db.session.commit()
            return make_response ( [], 200)
        else :
            return make_response ( {"error": "Restaurant not found"}, 404 )

api.add_resource( RestaurantById, '/restaurants/<int:id>', endpoint='restaurant_by_id' )



class Pizza ( Resource ) :
    def get_pizza ( self ) :
        pizzas = [pizza.to_dict() for pizzas in Pizza.query.all()]
        return make_response( jsonify(pizzas), 200 )

api.add_resource(Pizza, '/pizzas', endpoint='pizzas')



class RestaurantPizza ( Resource ) :
    def post ( self ) :
        new_record = RestaurantPizza (
            price = request.get_json()['price'],
            pizza_id = request.get_json()['pizza_id'],
            restaurant_id = request.get_json()['restaurant_id']
        )
        db.session.add(new_record)
        db.session.commit()
        
        response_body =new_record.to_dict()
        response = make_response ( jsonify(response_body), 201 )

        # NEEDS FIX
        if new_record != None :
            response = make_response ( jsonify(response_body), 201 )
        else :
            response = make_response ( jsonify(response_body), 400 )
        return response

api.add_resource( RestaurantPizza, '/restaurantpizza', endpoint='restaurantpizza')



if __name__ == "__main__":
    app.run(port=5555, debug=True)
