from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)

db = mongo.db.items

# Create (POST)
@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    item_id = db.insert_one(data).inserted_id
    return jsonify({"message": "Item added", "id": str(item_id)})

# Read (GET)
@app.route('/items', methods=['GET'])
def get_items():
    items = [{"_id": str(item["_id"]), "name": item["name_item"], "price": item["price"]} for item in db.find()]
    return jsonify(items)

@app.route('/items/<id>', methods=['GET'])
def get_item(id):
    item = db.find_one({"_id": ObjectId(id)})
    if item:
        return jsonify({"_id": str(item["_id"]), "name": item["name_item"], "price": item["price"]})
    return jsonify({"error": "Item not found"}), 404

# Update (PUT)
@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    data = request.json
    db.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Item updated"})

# Delete (DELETE)
@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    db.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Item deleted"})

if __name__ == '__main__':
    app.run(debug=True)
