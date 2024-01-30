#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
# from flask_cors import CORS


app = Flask(__name__)

# Use a relative path to create the SQLite database in the same directory as your code
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Disable SQLAlchemy track modifications to suppress a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "<h1>Superheroes</h1>"

@app.route('/heroes', methods=["GET"])
def heroes():
    if request.method == "GET":
        heros = Hero.query.all()
        hero_list = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heros]
        return jsonify(hero_list)


@app.route('/heroes/<int:id>', methods=["GET"])
def heroes_id(id):
    if request.method == "GET":
        hero = Hero.query.get(id)

        if not hero:
            return jsonify({"error": f"Hero with ID {id} not found"}), 404

        hero_powers = HeroPower.query.filter_by(hero_id=id).all()
        power_list = []

        for hero_power in hero_powers:
            power = Power.query.get(hero_power.power_id)
            if power:
                power_obj = {
                    "id": power.id,
                    "name": power.name,
                    "description": power.description,  # Changed to "description"
                }
                power_list.append(power_obj)

        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,  # Changed to "super_name"
            "powers": power_list,  # Changed to "powers"
        }

        return jsonify(hero_data)
@app.route('/powers', methods=["GET"])
def powers():
    if request.method == "GET":
        powers = Power.query.all()
        power_list = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
        return jsonify(power_list)
    
@app.route('/powers/<int:id>',methods=["GET","PATCH"])
def powers_id(id):
    if request.method == "GET":
        power=Power.query.get(id)

        if not power :
           return jsonify({"error": f"Power with ID {id} not found"}),  
        else :
            power_list =[{"id":power.id, "name":power.name, "description":power.description}]
            return jsonify(power_list)
    
    if request.method == "PATCH":
        power = Power.query.get(id)

        if not power:
            return jsonify({"error": f"Power with ID {id} not found"}), 404

        # Ensure that the request content type is JSON
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Please use JSON."}), 415

        # Get the data to update from the request
        data = request.get_json()

        # Update the Power object with the new data
        if 'name' in data:
            power.name = data['name']

        if 'description' in data:
            power.description = data['description']

        # Commit the changes to the database
        db.session.commit()

        # Return a response indicating success
        return jsonify({"message": f"Power with ID {id} updated successfully"})

@app.route('/hero_powers', methods=["POST"])
def post_heropowers():
    if request.method == "POST":
        try:
            data = request.get_json()

            strength = data.get('strength')
            power_id = data.get('power_id')
            hero_id = data.get('hero_id')

            power = Power.query.get(power_id)
            hero = Hero.query.get(hero_id)

            if not power:
                return jsonify({"message": f"Power with ID {power_id} not found"}), 404

            if not hero:
                return jsonify({"message": f"Hero with ID {hero_id} not found"}), 404

            new_hero_power = HeroPower(
                strength=strength,
                power_id=power_id,
                hero_id=hero_id
            )

            db.session.add(new_hero_power)
            db.session.commit()

            return jsonify({})
        except Exception as e:
            return jsonify({"error": "Error occurred"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555)