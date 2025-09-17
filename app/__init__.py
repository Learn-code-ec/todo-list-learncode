import os
from flask import Flask
from datetime import datetime

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_HOST=os.environ.get('FLASK_DABATASE_HOST'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE=os.environ.get('FLASK_DATABASE')
    )
    
    from . import db
    db.init_app(app)

    from . import todo
    from . import auth

    app.register_blueprint(todo.bp)
    app.register_blueprint(auth.bp)

    @app.context_processor
    def inject_year():
        return {'year': datetime.now().year}
    
    return app
 