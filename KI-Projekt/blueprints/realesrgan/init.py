from flask import Blueprint

realesrgan_bp = Blueprint('realesrgan', __name__)

from . import routes
