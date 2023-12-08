from flask import Flask, jsonify, request
import json
import utils

app = Flask("Delta")

ALLIES = json.load(open(utils.get_absolute_path("/input/allies.json"), "r"))
ENEMY = json.load(open(utils.get_absolute_path("/input/enemy.json"), "r"))

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Delta simulaton API 1.0"}), 200

@app.route('/api/allies', methods=['GET'])
def get_allies():
    # Replace with your logic to get data
    return jsonify({"data": ALLIES}), 200

@app.route('/api/enemy', methods=['GET'])
def get_enemy():
    # Replace with your logic to get data
    return jsonify({"data": ENEMY}), 200

if __name__ == '__main__':
    app.run(debug=True)