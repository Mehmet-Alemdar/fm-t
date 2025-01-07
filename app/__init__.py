from flask import Flask
from mongoengine import connect
from app.routes import authors, books

def create_app():
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
        'db': 'example_db',
        'host': 'localhost',
        'port': 27017
    }
    connect(**app.config['MONGODB_SETTINGS'])

    # Register Blueprints
    app.register_blueprint(authors.bp, url_prefix='/authors')
    app.register_blueprint(books.bp, url_prefix='/books')

    return app