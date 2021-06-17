from datetime import datetime
import os

from flask import Flask, request, render_template, jsonify
from werkzeug.exceptions import HTTPException

from app import database, routes, brand
from app.helpers import user_manager


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///./database/app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # flask_login initialization
    user_manager.init_app(app)

    # database initialization
    database.init_app(app)

    routes.register_blueprints(app)
    app.add_url_rule('/', 'index')

    app.jinja_env.add_extension('jinja2.ext.do')

    @app.template_filter()
    def currency_float(value):
        return "{:,.2f}".format(value)

    @app.context_processor
    def inject_context():
        return dict(year=datetime.utcnow().year, brand=brand)

    @app.errorhandler(HTTPException)
    def unauthorized_error(error: HTTPException):
        if request.path.startswith('/api'):
            return jsonify(
                dict(message=error.name, description=error.description, status=error.code)
            ), error.code

        return render_template('error.html', error=error), error.code

    return app