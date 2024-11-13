""" imports """
from flask import Flask, render_template
from datetime import timedelta
from database import config 
from database.db import db 
from secure.jwt_setup import jwt 
from flask_sqlalchemy import SQLAlchemy 
from routes.auth_route import authRoute
from routes.user_route import userRoute

""" initalisations and configs """

# initalise flask app 
app = Flask(__name__, template_folder='templates', static_folder='static')

# config SQLAchemy from database/config.py 
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = True

# config JWT token cookies 
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# initalise jwt with flask app from secure/jwt_setup.py 
jwt.init_app(app)

# initalise database with flask instance 
db.init_app(app)
with app.app_context(): 
    db.create_all()

# register routes from app/routes directory 
app.register_blueprint(authRoute)
app.register_blueprint(userRoute)

""" Main page """
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)