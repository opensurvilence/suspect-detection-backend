from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
import os

from .routes import login, suspects

app = Flask(__name__)
app.config['PORT'] = 5000
app.config['DEBUG'] = True
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
JWT = JWTManager(app)

app.register_blueprint(login.login)
app.register_blueprint(suspects.suspects)


@app.route('/')
def home():
    return "You are on suspect detection backend root route "


if __name__ == '__main__':
    print("running...")
    app.run(debug=True, port=5001)
