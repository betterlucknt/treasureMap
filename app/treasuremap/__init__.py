from flask import Blueprint

bp = Blueprint('treasuremap', __name__)

from app.treasuremap import routes
