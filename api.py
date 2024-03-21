from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient()
db_name = client['CreditCard']

app = Flask(__name__)

@app.route('/')
def home():
    return "hello"


# "http://172.43.0.69:5000/get-gps-location"

@app.route('/get-gps-location', methods=['POST'])
def get_gps_location():
    data = request.get_json()
    db_collections_coord = db_name['coord']
    try:
        db_collections_coord.insert_one(data)
        return jsonify({"message": "Succcess"}), 200
    except DuplicateKeyError:
        filter = {'_id': data['_id']}
        update = {'$set': {'latitude': data['latitude'], 'longitude': data['longitude']}, }
        result = db_collections_coord.update_one(filter, update)
        return jsonify({"message": "Update Succcess"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")