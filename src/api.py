from flask import Flask
from flask_cors import CORS
from controller import create_controller
from error_handler import create_error_handler
from database.models import db_drop_and_create_all, setup_db

app = Flask(__name__)
with app.app_context():
    create_controller(app)
    create_error_handler(app)
    setup_db(app)
    db_drop_and_create_all()
    CORS(app)


if __name__ == "__main__":
    app.debug = True
    app.run()
