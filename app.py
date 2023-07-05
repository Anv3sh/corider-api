from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Users'
mongo = PyMongo(app)
api = Api(app)

# User resource
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = mongo.db.user.find_one_or_404({'_id': ObjectId(user_id)}, {'password': 0})
            return {'id': str(user['_id']), 'name': user['name'], 'email': user['email']}
        else:
            users = mongo.db.user.find({}, {'password': 0})
            return [{'id': str(user['_id']), 'name': user['name'], 'email': user['email']} for user in users]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        data = parser.parse_args()
        new_user = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password']
        }
        result = mongo.db.user.insert_one(new_user)
        return {'id': str(result.inserted_id), 'name': new_user['name'], 'email': new_user['email']}, 201

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        data = parser.parse_args()
        updated_user = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password']
        }
        result = mongo.db.user.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user})
        if result.modified_count == 0:
            return {'error': 'User not found'}, 404
        return {'id': user_id, 'name': updated_user['name'], 'email': updated_user['email']}

    def delete(self, user_id):
        result = mongo.db.user.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count == 0:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted'}

# Add resource routes
api.add_resource(UserResource, '/users', '/users/<string:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
