from flask import Blueprint

bp = Blueprint('system', __name__, url_prefix='/api')

from app.system.api_v1 import api as v4

v4.register(bp)
