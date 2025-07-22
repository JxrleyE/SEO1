from flask import Blueprint

# Create a Blueprint for the home route
home_bp = Blueprint('home', __name__)

# Import routes to register the endpoints
from . import routes

