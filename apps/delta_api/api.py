from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import common.units as units

import json
import utils
from common.units import OBJECT_TO_CLASS_MAPPER
import random

class forces():
    def __init__(self, dicts):
        self.units = dicts

    def unitsCount(self, kind):
        return len([unit for unit in self.units if unit['object_name'].startswith(kind)])

    def set_unitCount(self, kind, count):
        unitsCount = self.unitsCount(kind)

        if count > unitsCount:
            for i in range(count - unitsCount):
                unit = {"object_name": kind, 
                        "location": {"longtitude": random.randint(18, 19), "latitude": random.randint(0, 19)},
                        "object_confidence": 0.8,
                        "located_by": "drone1697i2bg335",
                }
                self.units.append(unit)
        elif count < unitsCount:
            these = [unit for unit in self.units if unit['object_name'].startswith(kind)]
            no_these = [unit for unit in self.units if not unit['object_name'].startswith(kind)]
            for i in range(len(these) - count):
                these.pop()
            self.units = these + no_these

    def tanksCount(self):
        return self.unitsCount("tank")

    def set_tanksCount(self, count):
        self.set_unitCount("tank", count)

    def infantryCount(self):
        return self.unitsCount("stormtrooper")

    def set_infantryCount(self, count):
        self.set_unitCount("stormtrooper", count)

    def machinegunnerCount(self):
        return self.unitsCount("machinegunner")

    def set_machinegunnerCount(self, count):
        self.set_unitCount("machinegunner", count)


app = Flask("Delta")
def run():
    CORS(app)
    app.run(debug=True)

ALLIES = forces(json.load(open(utils.get_absolute_path("/input/allies.json"), "r")).get("forces"))
ENEMY = forces(json.load(open(utils.get_absolute_path("/input/enemy.json"), "r")).get("forces"))

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Delta simulaton API 1.0"}), 200

@app.route('/api/allies', methods=['GET'])
def get_allies():
    return jsonify({"data": {"forces": ALLIES.units}}), 200

@app.route('/api/enemy', methods=['GET'])
def get_enemy():
    return jsonify({"data": {"forces": ENEMY.units}}), 200

@app.route('/api/enemy/tanksCount', methods=['GET'])
@cross_origin()
def get_enemyTanks():
    return jsonify({"data": ENEMY.tanksCount()}), 200

@app.route('/api/enemy/tanksCount', methods=['POST'])
@cross_origin()
def set_enemyTanks():
    data = request.get_json()
    if 'count' in data:
        ENEMY.set_tanksCount(data['count'])
        
        return jsonify({"message": "Count of tanks has been set"}), 200
    else:
        return jsonify({"message": "No count provided"}), 400

@app.route('/api/enemy/infantryCount', methods=['GET'])
@cross_origin()
def get_enemyInfantry():
    return jsonify({"data": ENEMY.infantryCount()}), 200

@app.route('/api/enemy/infantryCount', methods=['POST'])
@cross_origin()
def set_enemyInfantry():
    data = request.get_json()
    if 'count' in data:
        ENEMY.set_infantryCount(data['count'])
        
        return jsonify({"message": "Count of infantry has been set"}), 200
    else:
        return jsonify({"message": "No count provided"}), 400

@app.route('/api/enemy/machinegunnerCount', methods=['GET'])
@cross_origin()
def get_enemyMachinegunner():
    return jsonify({"data": ENEMY.machinegunnerCount()}), 200

@app.route('/api/enemy/machinegunnerCount', methods=['POST'])
@cross_origin()
def set_enemyMachinegunner():
    data = request.get_json()
    if 'count' in data:
        ENEMY.set_machinegunnerCount(data['count'])
        
        return jsonify({"message": "Count of machinegunners has been set"}), 200
    else:
        return jsonify({"message": "No count provided"}), 400
