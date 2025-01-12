from .views import auth_blueprint

def init_app(app):
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
