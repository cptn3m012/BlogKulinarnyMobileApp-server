from flask import Flask


def create_app():
    app = Flask(__name__)

    # Importuj i rejestruj blueprinty
    from .routes import authentication, user_management, recipes, categories, comments
    app.register_blueprint(authentication.bp)
    app.register_blueprint(user_management.bp)
    app.register_blueprint(recipes.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(comments.bp)

    return app
