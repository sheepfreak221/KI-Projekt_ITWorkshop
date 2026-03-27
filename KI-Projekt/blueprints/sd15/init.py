from flask import Blueprint

sd15_bp = Blueprint('sd15', __name__)

from . import routes