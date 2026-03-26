from flask import Blueprint

bert_bp = Blueprint('bert', __name__)

from . import routes
