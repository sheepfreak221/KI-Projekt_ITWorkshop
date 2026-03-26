from flask import Blueprint

coqui_bp = Blueprint('coqui', __name__)

from . import routes
