from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Users'
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    result = mongo.db.user.insert_one(new_user)
    return jsonify({'id': str(result.inserted_id), 'name': new_user['name'], 'email': new_user['email']}), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.user.find({}, {'password': 0}) 
    return jsonify([{'id': str(user['_id']), 'name': user['name'], 'email': user['email']} for user in users])


@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = mongo.db.user.find_one_or_404({'_id': ObjectId(user_id)}, {'password': 0}) 
    return jsonify({'id': str(user['_id']), 'name': user['name'], 'email': user['email']})

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    updated_user = {
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    result = mongo.db.user.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user})
    if result.modified_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user_id, 'name': updated_user['name'], 'email': updated_user['email']})

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = mongo.db.user.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted'})

if __name__ == '__main__':
    app.run(debug=True)
