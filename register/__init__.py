from flask import Blueprint

# Create a Blueprint for the register route
register_bp = Blueprint('register', __name__)

# Import routes to register the endpoints
from . import routes

