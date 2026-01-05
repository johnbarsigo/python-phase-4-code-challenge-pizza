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

db.init_app(app)

migrate = Migrate(app, db)


api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


class RestaurantList ( Resource ) :
    def get ( self ) :
        restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
        return make_response( jsonify(restaurants), 200 )

api.add_resource(RestaurantList, '/restaurants', endpoint='restaurants')

class RestaurantById ( Resource ) :
    def get ( self, id ) :

        # restaurant_match = [ Restaurant.query.filter_by(id=id).first().to_dict() ]
        # restaurant = Restaurant.query.filter_by(id=id).first()
        restaurant = Restaurant.query.get(id)

        if restaurant :
            return make_response( jsonify(restaurant.to_dict()), 200 )
        else :
            return make_response ( {"error": "Restaurant not found"}, 404 )
    
    def delete ( self, id ) :
        restaurant_match = Restaurant.query.filter_by(id=id).first()
        if restaurant_match :
            db.session.delete(restaurant_match)
            db.session.commit()
            return make_response ( '', 204)
        else :
            return make_response ( {"error": "Restaurant not found"}, 404 )

api.add_resource( RestaurantById, '/restaurants/<int:id>', endpoint='restaurant_by_id' )



class PizzaList ( Resource ) :
    def get ( self ) :
        pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
        return make_response( jsonify(pizzas), 200 )

api.add_resource(PizzaList, '/pizzas', endpoint='pizzas')



class RestaurantPizzaCreate ( Resource ) :
    def post ( self ) :
        try :
            data = request.get_json()
            new_record = RestaurantPizza (
                price = data['price'],
                pizza_id = data['pizza_id'],
                restaurant_id = data['restaurant_id'])

            db.session.add(new_record)
            db.session.commit()

            return make_response( jsonify(new_record.to_dict()), 201)
        except Exception as e :
            return make_response(
                jsonify({"errors": ["validation errors"]}),
                400
            )
        
        # response_body =new_record.to_dict()
        # response = make_response ( jsonify(response_body), 201 )

        # NEEDS FIX
        # if new_record != None :
        #     response = make_response ( jsonify(response_body), 201 )
        # else :
        #     response = make_response ( jsonify(response_body), 400 )
        # return response
        # return make_response( jsonify(new_record.to_dict()), 201)

api.add_resource( RestaurantPizzaCreate, '/restaurant_pizzas', endpoint='restaurant_pizzas')



if __name__ == "__main__":
    app.run(port=5555, debug=True)
