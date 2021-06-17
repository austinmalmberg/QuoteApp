
def register_blueprints(app):
    from . import index
    app.register_blueprint(index.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import api
    api.register_blueprints(app)
