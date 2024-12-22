import logging
import sys
from flask import Flask,jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database.db import initialize_db
from flask_restful import Api
from router.routes import initialize_routes
from configs.configurator import initconfig
from configs import settings
from datetime import timedelta
from utils.exception import CustomException
import os


app =Flask(__name__)

initconfig(env='dev')

# setting CORS content header
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app,resources={r'/api/v1/*': {"origins": "*"}})
api = Api(app,'/api/v1')


# adding jwt token config to app
app.config['JWT_SECRET_KEY'] =settings.jwt_secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
jwt = JWTManager(app)



# Custom error handler for missing authorization header
@jwt.unauthorized_loader
def custom_unauthorized_response(callback):
    logging.error(callback)

    return jsonify({
        "data": [],
        "status": "failed",
        "message": "Missing Authorization Header"
    }), 401

# Custom error handler for invalid tokens
@jwt.invalid_token_loader
def custom_invalid_token_response(callback):
    logging.error(callback)
    return jsonify({
        "data": [],
        "status": "failed",
        "message": "Invalid Token"
    }), 403

# Custom error handler for expired tokens
@jwt.expired_token_loader
def custom_expired_token_response(*args):
    logging.error('Token has expired')
    return jsonify({
        "data": [],
        "status": "failed",
        "message": "Token has expired"
    }), 401

# Error handler for Custom raise errors
@app.errorhandler(CustomException)
def handle_custom_exception(error):
    return error.response

# Connect to MongoDB
initialize_db()

# initialize routes
initialize_routes(api)
if __name__ == '__main__':

    app.run(debug=True,port=5001,host="0.0.0.0")

