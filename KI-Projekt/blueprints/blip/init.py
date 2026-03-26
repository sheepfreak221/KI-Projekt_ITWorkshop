from flask import Blueprint

blip_bp = Blueprint('blip', __name__)

from . import routes
