from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from entities import db
from flask_jwt_extended import JWTManager
from api import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    

    register_blueprints(app)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST
    )
