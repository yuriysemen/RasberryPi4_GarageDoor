"""
Initialize Flask application.
"""
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)

api = Api(app)
CORS(app)

# initialize routes
from app import routes

routes.init_routes(api)
