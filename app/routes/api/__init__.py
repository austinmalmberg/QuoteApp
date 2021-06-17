
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')


def register_blueprints(app):
    # registration of child blueprints within the API

    from . import user
    api_bp.register_blueprint(user.bp)

    # register the api blueprint
    app.register_blueprint(api_bp)


