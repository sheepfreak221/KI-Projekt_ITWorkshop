from flask import Blueprint

gpt2_bp = Blueprint('gpt2', __name__)

from . import routes
