import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .routes import login, suspects, user

app = Flask(__name__)
app.config['PORT'] = 5000
app.config['DEBUG'] = True
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
JWT = JWTManager(app)

app.register_blueprint(login.login)
app.register_blueprint(suspects.suspects)
app.register_blueprint(user.user)


@app.route('/')
def home():
    return "You are on suspect detection backend root route "


@app.route('/flask')
def flask():
    return "You are on the flask route "


if __name__ == '__main__':
    print("running...")
    app.run(host='0.0.0.0', port=5001)
