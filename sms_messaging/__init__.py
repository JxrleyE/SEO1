from flask import Blueprint


# create blueprint for /sms route
sms_bp = Blueprint('sms', __name__, url_prefix='/sms')


# importing routes.py to link up to blueprint
from . import routes
