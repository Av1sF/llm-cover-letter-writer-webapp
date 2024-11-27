""" imports """
import sys
sys.path.append('app')
from flask import Flask, render_template
from datetime import timedelta
from database.db import db 
from setup.jwt_setup import jwt 
from routes.auth_route import authRoute
from routes.user_route import userRoute
from routes.model_route import modelRoute
from os import environ

""" initalisations and configs """

# initalise flask app 
app = Flask(__name__, template_folder='templates', static_folder='static')

# config SQLAchemy from database/config.py 
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = True

# config JWT token cookies 
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# register routes from app/routes directory 
app.register_blueprint(modelRoute)
app.register_blueprint(authRoute)
app.register_blueprint(userRoute)

# initalise jwt with flask app from secure/jwt_setup.py 
jwt.init_app(app)

# initalise database with flask instance 
db.init_app(app)
with app.app_context(): 
    db.create_all()

""" Main page """
@app.route('/')
def home():
    return render_template("index.html"), 200 

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=5000)